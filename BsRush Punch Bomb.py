"""Define a simple example plugin."""

# ba_meta require api 9

from __future__ import annotations
from typing import TYPE_CHECKING
import babase
import bascenev1 as bs
import bascenev1lib

# by BsRush_Mod
# ---------------------------------------------
number_of_bombs = 30    # int 
punchs = True          # True or False
# ---------------------------------------------

# ba_meta export plugin
class PunchBombPlugin(babase.Plugin):
    """Bomb count and boxing gloves modifier plugin"""
    
    def __init__(self) -> None:
        super().__init__()
        
        self.apply_settings()
    
    def apply_settings(self) -> None:
        try:
            from bascenev1lib.actor.spaz import Spaz
            
            Spaz.default_bomb_count = number_of_bombs
            
            # Set boxing gloves based on configuration
            Spaz.default_boxing_gloves = punchs
            
            print(f"PunchBombPlugin: Bombs={number_of_bombs}, Punch={punchs}")
            
        except Exception as e:
            print(f"Error in PunchBombPlugin: {e}")