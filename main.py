from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder
from loguru import logger as log

from .actions.CellButton.CellButton import CellButton
from .actions.BackButton.BackButton import BackButton
from .actions.ScoreDisplay.ScoreDisplay import ScoreDisplay
from .actions.NewGame.NewGame import NewGame
from .actions.LaunchGame.LaunchGame import LaunchGame


class TicTacToe(PluginBase):
    def __init__(self):
        super().__init__()

        # Game state
        self.board = [""] * 9  # 9 cells, empty string = no player
        self.current_player = "X"
        self.game_over = False
        self.winner = None
        self.score_x = 0
        self.score_o = 0

        # Registered actions for updates
        self.cell_actions = []
        self.score_actions = []

        # Back page tracking
        self.back_page = None

        # Register actions
        self.cell_button_holder = ActionHolder(
            plugin_base=self,
            action_base=CellButton,
            action_id="com_pol_tictactoe::CellButton",
            action_name="Case du jeu",
        )
        self.add_action_holder(self.cell_button_holder)

        self.back_button_holder = ActionHolder(
            plugin_base=self,
            action_base=BackButton,
            action_id="com_pol_tictactoe::BackButton",
            action_name="Retour",
        )
        self.add_action_holder(self.back_button_holder)

        self.score_display_holder = ActionHolder(
            plugin_base=self,
            action_base=ScoreDisplay,
            action_id="com_pol_tictactoe::ScoreDisplay",
            action_name="Score",
        )
        self.add_action_holder(self.score_display_holder)

        self.new_game_holder = ActionHolder(
            plugin_base=self,
            action_base=NewGame,
            action_id="com_pol_tictactoe::NewGame",
            action_name="Nouvelle partie",
        )
        self.add_action_holder(self.new_game_holder)

        self.launch_game_holder = ActionHolder(
            plugin_base=self,
            action_base=LaunchGame,
            action_id="com_pol_tictactoe::LaunchGame",
            action_name="Lancer Tic-Tac-Toe",
        )
        self.add_action_holder(self.launch_game_holder)

        self.register(
            plugin_name="Tic-Tac-Toe",
            github_repo="https://github.com/pol/streamcontroller-tictactoe",
            plugin_version="1.0.0",
            app_version="1.5.0-beta.6"
        )

    def play_cell(self, cell_index: int) -> bool:
        """Play a cell. Returns True if the move was valid."""
        if self.game_over or self.board[cell_index] != "":
            return False

        self.board[cell_index] = self.current_player

        if self.check_winner():
            self.game_over = True
            self.winner = self.current_player
            if self.current_player == "X":
                self.score_x += 1
            else:
                self.score_o += 1
            log.info(f"Winner: {self.winner}")
        elif "" not in self.board:
            self.game_over = True
            self.winner = None  # Draw
            log.info("Draw!")
        else:
            self.current_player = "O" if self.current_player == "X" else "X"

        self.update_all_cells()
        self.update_all_scores()
        return True

    def check_winner(self) -> bool:
        """Check if current player has won."""
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        for pattern in win_patterns:
            if all(self.board[i] == self.current_player for i in pattern):
                return True
        return False

    def reset_game(self):
        """Reset the game board for a new game."""
        self.board = [""] * 9
        self.current_player = "X"
        self.game_over = False
        self.winner = None
        self.update_all_cells()
        self.update_all_scores()
        log.info("Game reset")

    def reset_scores(self):
        """Reset the scores."""
        self.score_x = 0
        self.score_o = 0
        self.update_all_scores()

    def register_cell_action(self, action):
        if action not in self.cell_actions:
            self.cell_actions.append(action)

    def unregister_cell_action(self, action):
        if action in self.cell_actions:
            self.cell_actions.remove(action)

    def register_score_action(self, action):
        if action not in self.score_actions:
            self.score_actions.append(action)

    def unregister_score_action(self, action):
        if action in self.score_actions:
            self.score_actions.remove(action)

    def update_all_cells(self):
        for action in self.cell_actions:
            try:
                action.update_display()
            except Exception as e:
                log.error(f"Error updating cell: {e}")

    def update_all_scores(self):
        for action in self.score_actions:
            try:
                action.update_display()
            except Exception as e:
                log.error(f"Error updating score: {e}")
