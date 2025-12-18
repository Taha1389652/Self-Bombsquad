import bascenev1 as bs
import babase

# ba_meta require api 9
# ba_meta export babase.Plugin


class SuperPunchJumpBsRush(babase.Plugin):
    def on_app_running(self) -> None:
        from bascenev1lib.actor import spaz

        original_punch = spaz.Spaz.on_punch_press
        
        def new_on_punch_press(self):
            if original_punch:
                original_punch(self)

            if not self.node or not self.node.exists():
                return

            pos = self.node.position
            vel = self.node.velocity

            self.node.handlemessage(
                "impulse",
                pos[0], pos[1] + 1.0, pos[2],
                vel[0], vel[1], vel[2],
                80, 20, 0, 0,
                vel[0], vel[1] + 12, vel[2]
            )

            self.node.punch_pressed = True

            try:
                bs.getsound('powerup01').play(volume=0.3)
            except:
                pass

        spaz.Spaz.on_punch_press = new_on_punch_press
