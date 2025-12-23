# Gaming Library API

A REST API for managing gaming libraries, writing reviews, and discovering games. Built with FastAPI, SQLAlchemy, and JWT authentication.

## Features

- 🎮 Browse 700+ scraped games
- 🔐 User authentication with JWT tokens  
- 📚 Personal gaming library management
- ⭐ Game reviews and ratings
- 🔍 Search and filter games by genre, rating
- 📊 Top-rated and most-played games

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Database with 700+ games
- **JWT** - Token-based authentication
- **Scrapy** - Web scraping for game data

## API Endpoints

### Authentication
- `POST /user/` - Register new user
- `POST /login/` - Login and get token

### Games
- `GET /games/` - List all games
- `GET /games/single/{title}` - Get game details
- `GET /search/{title}/` - Search games
- `GET /games/top_rated/` - Top rated games
- `GET /games/most_played/` - Most played games
- `GET /games/genres/` - Filter by genre

### Library
- `POST /library/` - Add game to library (secured)
- `GET /library/` - Get your library (secured)
- `PATCH /library/{game_title}` - Update game status (secured)
- `DELETE /library/{game_title}` - Remove from library (secured)

### Reviews
- `POST /review/` - Write review (secured)
- `GET /reading_rev/{title}` - Get game reviews
- `PATCH /review/{game_title}` - Update review (secured)
- `DELETE /review_del/{game_title}` - Delete review (secured)

## Setup

1. **Clone the repository**
```bash
   git clone https://github.com/YOUR_USERNAME/gaming-library.git
   cd gaming-library
```

2. **Install dependencies**
```bash
   pip install -r requirements.txt
```

3. **Run the API**
```bash
   cd api
   uvicorn main:app --reload
```

4. **Access API documentation**
   - Interactive docs: `http://localhost:8000/docs`
   - Alternative docs: `http://localhost:8000/redoc`

## Authentication

Secured endpoints require a JWT token:

1. Register: `POST /user/`
2. Login: `POST /login/` (returns access token)
3. Use token in requests: `?token=YOUR_TOKEN`

## Database Schema

- **Users** - User accounts with hashed passwords
- **Games** - 700+ games with details (title, rating, genres, etc.)
- **Reviews** - User reviews with ratings
- **UserLibrary** - User's gaming library with status tracking

## Project Structure
```
backloged/
├── api/              # FastAPI application
│   ├── main.py       # API routes
│   ├── auth.py       # Authentication logic
│   ├── database.py   # Database config
│   ├── models.py     # SQLAlchemy models
│   └── schemas.py    # Pydantic schemas
├── backloged/        # Scrapy project
│   └── spiders/      # Game data scraper
│       └── backlooged.db  # SQLite database
└── README.md
```

## Future Improvements

- [ ] Add pagination to game lists
- [ ] Implement proper error handling with HTTP status codes
- [ ] Add rate limiting
- [ ] Write unit tests
- [ ] Add user statistics endpoint
- [ ] Deploy to production with PostgreSQL

## Author

Built as a portfolio project to demonstrate full-stack backend development skills.
