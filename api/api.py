from typing import List
from typing_extensions import TypedDict
from django.db.models import Q
from django.utils import timezone
from ninja import ModelSchema, Redoc, Schema
from ninja_extra import ControllerBase, NinjaExtraAPI, api_controller, route, pagination
from datetime import datetime
from django.contrib.auth import get_user_model
from news.models import NewsItem
from bs4 import BeautifulSoup
from django.utils import text
from frontend.models import Sponsor
import random
from django.db.models import Q
from teams.models import Team, TeamMembership, Season, TeamPicture
from itertools import chain
from activities.models import Game, Opponent

api = NinjaExtraAPI(title="clubmanager", docs=Redoc())


class SponsorSchema(ModelSchema):
    logo: str
    width: int
    height: int
    id: int

    class Config:
        model = Sponsor
        model_fields = ["name", "url"]

    @staticmethod
    def resolve_logo(obj: Sponsor) -> str:
        return obj.logo.url

    @staticmethod
    def resolve_width(obj: Sponsor) -> int:
        return obj.logo.width

    @staticmethod
    def resolve_height(obj: Sponsor) -> int:
        return obj.logo.height

    @staticmethod
    def resolve_id(obj: Sponsor) -> int:
        return obj.id


class PictureSchema(Schema):
    url: str
    width: int
    height: int


class NewsItemSchema(ModelSchema):
    teams: List[str]
    summary: str
    content: str
    main_picture: PictureSchema | None
    pictures: List[PictureSchema] | List

    class Config:
        model = NewsItem
        model_fields = ["title", "slug", "publish_on"]

    @staticmethod
    def resolve_main_picture(obj: NewsItem):
        if obj.main_picture() is not None:
            return {
                "url": obj.main_picture().picture.url,
                "height": obj.main_picture().picture.height,
                "width": obj.main_picture().picture.width,
            }

    @staticmethod
    def resolve_picutres(obj: NewsItem):
        return [{"url": picture.picture.url, "height": picture.picture.height, "width": picture.picture.height} for picture in obj.pictures.exclude(main_picture=True).all()]

    @staticmethod
    def resolve_picture_height(obj: NewsItem):
        if obj.main_picture() is not None:
            return obj.main_picture().picture.height

        return 0

    @staticmethod
    def resolve_picture_width(obj: NewsItem):
        if obj.main_picture() is not None:
            return obj.main_picture().picture.width

        return 0

    @staticmethod
    def resolve_teams(obj: NewsItem):
        return [team.short_name for team in obj.teams.all()]

    @staticmethod
    def resolve_content(obj: NewsItem):
        return obj.formatted()

    @staticmethod
    def resolve_summary(obj: NewsItem):
        summary = BeautifulSoup(obj.formatted(), "html.parser")

        for img in summary.find_all("img"):
            if len(img.parent.contents) == 1:
                img.parent.decompose()
            else:
                img.decompose()

        return text.Truncator(summary).words(40, html=True)

    @staticmethod
    def resolve_pictures(obj: NewsItem):
        return [picture.picture.url for picture in obj.pictures.exclude(main_picture=True).all()]


class TeamSchema(ModelSchema):
    logo: str

    class Config:
        model = Team
        model_fields = ["name"]

    @staticmethod
    def resolve_name(obj: Team):
        return obj.short_name

    @staticmethod
    def resolve_logo(obj: Team):
        return ""


class OpponentSchema(ModelSchema):
    class Config:
        model = Opponent
        model_fields = ["name", "logo"]

    @staticmethod
    def resolve_logo(obj: Team):
        return obj.logo.url


class GameSchema(ModelSchema):
    team: TeamSchema
    opponent: OpponentSchema
    is_home_game: bool

    class Config:
        model = Game
        model_fields = ["team", "opponent", "date", "location"]

    @staticmethod
    def resolve_is_home_game(obj: Game):
        return obj.is_home_game


@api_controller("/sponsors")
class SponsorController(ControllerBase):
    @route.get("", response={200: List[SponsorSchema]})
    def get_sponsors(self):
        sponsors = list(Sponsor.objects.filter(start_date__lte=timezone.now()).filter(Q(end_date__gte=timezone.now()) | Q(end_date=None)))
        random.shuffle(sponsors)
        return sponsors


@api_controller("/news")
class NewsController(ControllerBase):
    @route.get("", response={200: pagination.PaginatedResponseSchema[NewsItemSchema]})
    @pagination.paginate(pagination.PageNumberPaginationExtra, page_size=8)
    def get_news(self):
        return (
            NewsItem.objects.filter(status=NewsItem.StatusChoices.RELEASED, publish_on__lte=timezone.now())
            .exclude(type=NewsItem.NewsItemTypeChoices.INTERNAL)
            .order_by("-publish_on")
        )

    @route.get("{slug}", response={200: NewsItemSchema})
    def get_news_by_slug(self, slug: str):
        return NewsItem.objects.exclude(type=NewsItem.NewsItemTypeChoices.INTERNAL).get(status=NewsItem.StatusChoices.RELEASED, publish_on__lte=timezone.now(), slug=slug)


@api_controller("/games")
class GamesController(ControllerBase):
    @route.get("", response={200: List[GameSchema]})
    def get_games(self, team: str = "all", count: int = 5, home_games_only: bool = False):
        games = Game.objects.filter(date__gte=timezone.now())

        if team != "all":
            games = games.filter(team__slug=team)

        if home_games_only:
            games = games.filter(Q(location__iexact="ice skating center mechelen") | Q(location__iexact="iscm"))

        return games[:count]


api.register_controllers(SponsorController, NewsController, GamesController)

""" 
class BlackoutSchema(Schema):
    end: datetime


class AuthorSchema(ModelSchema):
    class Config:
        model = get_user_model()
        model_fields = ["first_name", "last_name"]


class NewsSchema(ModelSchema):
    author: AuthorSchema
    picture: str | None
    teams: List[str]
    summary: str
    picture_slot: str
    pictures: List[str]
    picture_height: int | None
    picture_width: int | None
    publish_date: datetime
    content: str

    class Config:
        model = NewsItem
        model_fields = ["slug", "title", "author", "teams"]

    @staticmethod
    def resolve_picture(obj: NewsItem):
        if obj.main_picture() is not None:
            return obj.main_picture().picture.url

        return None

    @staticmethod
    def resolve_picture_height(obj: NewsItem):
        if obj.main_picture() is not None:
            return obj.main_picture().picture.height

        return 0

    @staticmethod
    def resolve_picture_width(obj: NewsItem):
        if obj.main_picture() is not None:
            return obj.main_picture().picture.width

        return 0

    @staticmethod
    def resolve_picture_slot(obj: NewsItem):
        return "middle"

    @staticmethod
    def resolve_teams(obj: NewsItem):
        return [team.short_name for team in obj.teams.all()]

    @staticmethod
    def resolve_content(obj: NewsItem):
        return obj.formatted()

    @staticmethod
    def resolve_summary(obj: NewsItem):
        summary = BeautifulSoup(obj.formatted(), "html.parser")

        for img in summary.find_all("img"):
            if len(img.parent.contents) == 1:
                img.parent.decompose()
            else:
                img.decompose()

        return text.Truncator(summary).words(40, html=True)

    @staticmethod
    def resolve_pictures(obj: NewsItem):
        return [picture.picture.url for picture in obj.pictures.exclude(main_picture=True).all()]

    @staticmethod
    def resolve_publish_date(obj: NewsItem):
        return obj.publish_on

    @staticmethod
    def resolve_text(obj: NewsItem):
        return obj.formatted()


class SponsorSchema(ModelSchema):
    logo: str

    class Config:
        model = Sponsor
        model_fields = ["name", "url"]

    @staticmethod
    def resolve_logo(obj: Sponsor):
        return obj.logo.url


class TeamMenuSchema(Schema):
    name: str
    slug: str


class TeamMemberSchema(ModelSchema):
    first_name: str
    last_name: str
    birth_year: int | None
    license_number: str
    alternate_captain: bool

    class Config:
        model = TeamMembership
        model_fields = ["captain", "role", "number"]

    @staticmethod
    def resolve_first_name(obj):
        return obj.member.first_name

    @staticmethod
    def resolve_last_name(obj):
        return obj.member.last_name

    @staticmethod
    def resolve_birth_year(obj):
        return obj.member.birthday.year

    @staticmethod
    def resolve_alternate_captain(obj):
        return obj.assistant_captain

    @staticmethod
    def resolve_license_number(obj):
        return obj.member.license


class TeamInfo(TypedDict):
    name: str
    full_name: str
    logo: str


class GameSchema(Schema):
    team: TeamInfo
    opponent: TeamInfo
    is_home_game: bool
    season: str | None
    rbihf_url: str | None
    date: datetime
    location: str
    number: str


class TeamSchema(ModelSchema):
    picture: str | None
    goalie: List[TeamMemberSchema]
    forward: List[TeamMemberSchema]
    defense: List[TeamMemberSchema]
    players: List[TeamMemberSchema]
    staff: List[TeamMemberSchema]
    full_name: str
    name: str

    class Config:
        model = Team
        model_fields = ["slug"]

    @staticmethod
    def resolve_full_name(obj):
        return obj.name

    @staticmethod
    def resolve_name(obj):
        return obj.short_name

    @staticmethod
    def resolve_picture(obj: Team):
        try:
            return obj.teampicture_set.get(season=Season.get_season()).picture.url
        except TeamPicture.DoesNotExist:
            return None

    @staticmethod
    def resolve_goalie(obj: Team):
        return obj.teammembership_set.filter(season=Season.get_season()).filter(role__abbreviation="GO").order_by("number")

    @staticmethod
    def resolve_forward(obj: Team):
        return obj.teammembership_set.filter(season=Season.get_season()).filter(role__abbreviation="F").order_by("number")

    @staticmethod
    def resolve_defense(obj: Team):
        return obj.teammembership_set.filter(season=Season.get_season()).filter(role__abbreviation="D").order_by("number")

    @staticmethod
    def resolve_players(obj: Team):
        return obj.teammembership_set.filter(season=Season.get_season()).filter(role=None).order_by("number")

    @staticmethod
    def resolve_staff(obj: Team):
        head_coach = obj.teammembership_set.filter(season=Season.get_season(), role__abbreviation="CO").order_by(
            "member__user__last_name", "member__user__first_name", "member__license"
        )
        assistant_coach = obj.teammembership_set.filter(season=Season.get_season(), role__abbreviation="AC").order_by(
            "member__user__last_name", "member__user__first_name", "member__license"
        )
        general_manager = obj.teammembership_set.filter(season=Season.get_season(), role__abbreviation="GM").order_by(
            "member__user__last_name", "member__user__first_name", "member__license"
        )
        team_manager = obj.teammembership_set.filter(season=Season.get_season(), role__abbreviation="TM").order_by(
            "member__user__last_name", "member__user__first_name", "member__license"
        )
        others = (
            obj.teammembership_set.filter(season=Season.get_season(), number=None)
            .exclude(
                Q(role__abbreviation="GO")
                | Q(role__abbreviation="F")
                | Q(role__abbreviation="D")
                | Q(role__abbreviation="CO")
                | Q(role__abbreviation="AC")
                | Q(role__abbreviation="GM")
                | Q(role__abbreviation="TM")
            )
            .order_by("member__user__last_name", "member__user__first_name", "member__license")
        )

        return list(chain(head_coach, assistant_coach, general_manager, team_manager, others))


@api_controller("/blackout")
class BlackoutController:
    @route.get("", response={200: BlackoutSchema | None})
    def get_blackout(self):
        return None


@api_controller("/news")
class NewsController:
    @route.get("", response={200: pagination.PaginatedResponseSchema[NewsSchema]})
    @pagination.paginate(pagination.PageNumberPaginationExtra, page_size=8)
    def get_news(self):
        return (
            NewsItem.objects.filter(status=NewsItem.StatusChoices.RELEASED, publish_on__lte=timezone.now())
            .exclude(type=NewsItem.NewsItemTypeChoices.INTERNAL)
            .order_by("-publish_on")
        )

    @route.get("{slug}", response={200: NewsSchema})
    def get_news_by_slug(self, slug: str):
        return NewsItem.objects.exclude(type=NewsItem.NewsItemTypeChoices.INTERNAL).get(status=NewsItem.StatusChoices.RELEASED, publish_on__lte=timezone.now(), slug=slug)


@api_controller("/sponsors")
class SponsorController:
    @route.get("", response={200: List[SponsorSchema]})
    def get_sponsors(self):
        sponsors = list(Sponsor.objects.filter(start_date__lte=timezone.now()).filter(Q(end_date__gte=timezone.now()) | Q(end_date=None)))
        random.shuffle(sponsors)
        return sponsors


@api_controller("/games")
class GamesController:
    @route.get("", response={200: List[GameSchema]})
    def get_games(self, limit: int = 0):
        return []


@api_controller("/team")
class TeamController:
    @route.get("/menu", response={200: List[TeamMenuSchema]})
    def get_teams_for_menu(self):
        return [
            {"name": "Lady Sharks BE", "slug": "lady-sharks-be"},
            {"name": "Div 1", "slug": "div-1"},
            {"name": "Div 2", "slug": "div-2"},
            {"name": "Div 3", "slug": "div-3"},
            {"name": "Div 4", "slug": "div-4"},
            {"name": "U16", "slug": "u16"},
            {"name": "U14", "slug": "u14"},
            {"name": "U12", "slug": "u12"},
            {"name": "U8/U10", "slug": "u8u10"},
        ]

    @route.get("{slug}", response={200: TeamSchema})
    def get_team_by_slug(self, slug: str):
        return Team.objects.get(slug=slug)


api.register_controllers(BlackoutController)
api.register_controllers(NewsController)
api.register_controllers(SponsorController)
api.register_controllers(GamesController)
api.register_controllers(TeamController)
 """
