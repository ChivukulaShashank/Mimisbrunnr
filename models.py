from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

# --- COMPONENT 1: ONGOING INSIGHTS (Composition) ---
class Annotation(BaseModel):
    """Raw thoughts, game dev insights, or art style notes."""
    content: str
    tag: str = "general"  # e.g., "mechanics", "art-style", "lore"
    timestamp: datetime = Field(default_factory=datetime.now)

# --- COMPONENT 2: FINAL EVALUATION (Composition) ---
class Review(BaseModel):
    """The final 'verdict' after finishing the media."""
    content: str
    completed_at: datetime = Field(default_factory=datetime.now)

# --- THE BASE MODEL (Abstraction & Inheritance Root) ---
class Media(ABC, BaseModel):
    title: str
    creator: str
    # Fields from your sketch
    total_parts: int = Field(gt=0, description="Total chapters/hours/episodes")
    completed_parts: int = Field(default=0, ge=0)
    final_rating: float = Field(ge=0, le=10)
    # Separation of Notes and Reviews
    notes: List[Annotation] = []
    final_review: Optional[Review] = None

    # Status % - Calculated automatically (Encapsulation)
    @property
    def status_percentage(self) -> float:
        if self.total_parts == 0: return 0.0
        return (self.completed_parts / self.total_parts) * 100

    @abstractmethod
    def get_type(self) -> str:
        """Forces subclasses to identify their category."""
        pass

# --- CONCRETE TYPES (Inheritance) ---
class Book(Media):
    def get_type(self): return "Literature"

class Movie(Media):
    def get_type(self): return "Cinema"

class VideoGame(Media):
    platform: str
    def get_type(self): return f"Game ({self.platform})"

class TV(Media):
    def get_type(self): return "TV Show"

class Anime(Media):
    def get_type(self): return "Anime"

# --- THE FRIDAY NIGHT SMOKE TEST ---
if __name__ == "__main__":
    # 1. Create a game entry
    my_game = VideoGame(
        title="Elden Ring", 
        creator="FromSoftware", 
        total_parts=100, 
        completed_parts=45, 
        platform="PC"
    )

    # 2. Add an ongoing note (Composition)
    my_game.notes.append(Annotation(
        content="The jagged boss designs are great reference for my Garuda project.",
        tag="art-style"
    ))

    # 3. Submit a Review (Only when finished)
    # my_game.final_review = Review(content="Masterpiece.", final_rating=10.0)

    print(f"--- {my_game.title} ---")
    print(f"Category: {my_game.get_type()}")
    print(f"Status: {my_game.status_percentage:.1f}%")
    print(f"Insights Count: {len(my_game.notes)}")
    if my_game.notes:
        print(f"Latest Insight: {my_game.notes[-1].content} [#{my_game.notes[-1].tag}]")