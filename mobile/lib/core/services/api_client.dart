import 'package:dio/dio.dart';
import 'package:retrofit/retrofit.dart';
import '../constants/app_constants.dart';
import '../../shared/models/user.dart';
import '../../shared/models/calendar.dart';
import '../../shared/models/todo.dart';
import '../../shared/models/vote.dart';
import '../../shared/models/event.dart';
import '../../shared/models/api_response.dart';

part 'api_client.g.dart';

@RestApi(baseUrl: AppConstants.apiBaseUrl)
abstract class ApiClient {
  factory ApiClient(Dio dio, {String baseUrl}) = _ApiClient;

  // Authentication endpoints
  @POST('/users/register')
  Future<AuthResponse> register(@Body() UserCreate user);

  @POST('/login/access-token')
  @FormUrlEncoded()
  Future<AuthResponse> login(
    @Field('username') String email,
    @Field('password') String password,
  );

  @POST('/auth/logout')
  Future<void> logout();

  @GET('/users/me')
  Future<User> getCurrentUser();

  // Calendar endpoints
  @GET('/calendars')
  Future<List<Calendar>> getCalendars();

  @POST('/calendars')
  Future<Calendar> createCalendar(@Body() CalendarCreate calendar);

  @GET('/calendars/{id}')
  Future<Calendar> getCalendar(@Path('id') int id);

  @PUT('/calendars/{id}')
  Future<Calendar> updateCalendar(
    @Path('id') int id,
    @Body() CalendarCreate calendar,
  );

  @DELETE('/calendars/{id}')
  Future<void> deleteCalendar(@Path('id') int id);

  // List endpoints
  @GET('/lists/calendar/{calendarId}')
  Future<List<TodoList>> getLists(@Path('calendarId') int calendarId);

  @POST('/lists/')
  Future<TodoList> createList(@Body() TodoListCreate list);

  @GET('/lists/{id}')
  Future<TodoList> getList(@Path('id') int id);

  @PUT('/lists/{id}')
  Future<TodoList> updateList(
    @Path('id') int id,
    @Body() TodoListCreate list,
  );

  @DELETE('/lists/{id}')
  Future<void> deleteList(@Path('id') int id);

  // List item endpoints
  @GET('/list-items/list/{listId}')
  Future<List<ListItem>> getListItems(@Path('listId') int listId);

  @POST('/list-items/')
  Future<ListItem> createListItem(@Body() ListItemCreate item);

  @GET('/list-items/{id}')
  Future<ListItem> getListItem(@Path('id') int id);

  @PUT('/list-items/{id}')
  Future<ListItem> updateListItem(
    @Path('id') int id,
    @Body() ListItemUpdate item,
  );

  @DELETE('/list-items/{id}')
  Future<void> deleteListItem(@Path('id') int id);

  // Vote endpoints
  @GET('/items/{itemId}/votes')
  Future<List<Vote>> getVotes(@Path('itemId') int itemId);

  @POST('/items/{itemId}/votes')
  Future<Vote> createVote(
    @Path('itemId') int itemId,
    @Body() VoteCreate vote,
  );

  @GET('/items/{itemId}/vote-stats')
  Future<VoteStats> getVoteStats(@Path('itemId') int itemId);

  @DELETE('/votes/{id}')
  Future<void> deleteVote(@Path('id') int id);

  // Event endpoints
  @GET('/calendars/{calendarId}/events')
  Future<List<Event>> getEvents(
    @Path('calendarId') int calendarId,
    @Query('start_date') String? startDate,
    @Query('end_date') String? endDate,
  );

  @POST('/calendars/{calendarId}/events')
  Future<Event> createEvent(
    @Path('calendarId') int calendarId,
    @Body() EventCreate event,
  );

  @GET('/events/{id}')
  Future<Event> getEvent(@Path('id') int id);

  @PUT('/events/{id}')
  Future<Event> updateEvent(
    @Path('id') int id,
    @Body() EventUpdate event,
  );

  @DELETE('/events/{id}')
  Future<void> deleteEvent(@Path('id') int id);
}