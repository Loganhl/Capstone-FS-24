from typing_tracker import TypingTracker

if __name__ == "__main__":
    tracker = TypingTracker()
    tracker.start_typing()
    tracker.calculate_metrics()