
from bot.configs import Questions, Quality, parse_config, parse_questions




if __name__ == '__main__':
    config = parse_config()
    questions = parse_questions(config)
    normalize_points(questions)
    print(questions)
