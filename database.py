import json
from igdb.wrapper import IGDBWrapper
from random import randint
from env import CLIENT_ID, APP_ID


wrapper = IGDBWrapper(CLIENT_ID, APP_ID)
game_infos = None

# Return two random dates, a minimum and maximum date.
def get_random_date():
  minimum_date = 791596800
  maximum_date = randint(791596800, 1107216000)
  return [minimum_date, maximum_date]

# Return a random game ID from IGDB
def get_random_game(dates):
  random_id_query = wrapper.api_request(
              'release_dates',
              f'fields date, category, game; where date > {dates[0]} & date < {dates[1]}; sort date desc; limit 1;'
            )
  # Convert the result from bytes to json
  result = json.loads(random_id_query.decode('utf-8'))
  if len(result) == 0:
      print("A API não retornou nenhum resultado.")
      return False
  game_id = result[0]['game']
  return game_id

# Return the info about the game with the random ID
def get_game_info(id):
  game_info_query = wrapper.api_request(
              'games',
              f'fields name, screenshots, first_release_date; where id={id}; limit 1;'
            )
  # Convert the result from bytes to json
  result = json.loads(game_info_query.decode('utf-8'))[0]
  if not 'screenshots' in result:
    print("Este jogo não possui screenshots. Selecionando novo jogo..")
    return None
  return [result['screenshots'][0], result['name']] 

# Return the URL of the screenshot with the given ID
def get_screenshot_url(screenshot_id):
  screenshot_query = wrapper.api_request(
      'screenshots',
      f'fields *; where id = {screenshot_id};'
  )
  # Convert the result from bytes to json
  result = json.loads(screenshot_query.decode('utf-8'))[0]
  return "http://" + result['url'][2:38] + "screenshot_huge" + result['url'][43:]


def all_game_info():
  random_date = get_random_date()
  random_game = get_random_game(random_date)
  game_info = get_game_info(random_game)
  if game_info:
    game_screenshot = get_screenshot_url(game_info[0])
    return [game_info, game_screenshot]