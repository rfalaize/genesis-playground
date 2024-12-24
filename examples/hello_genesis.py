import genesis as gs
from typing import NoReturn
from time import time

def main() -> NoReturn:
  gs.init(backend=gs.cpu)

  scene = gs.Scene(
    sim_options=gs.options.SimOptions(),
    viewer_options=gs.options.ViewerOptions(
      camera_pos=(3.5, 0.0, 2.5),
      camera_lookat=(0.0, 0.0, 0.5),
      camera_fov=40,
    ),
    show_viewer=True,
    rigid_options=gs.options.RigidOptions(
      dt=0.01,
      gravity=(0.0, 0.0, -10.0),
    ),
  )
  plane = scene.add_entity(gs.morphs.Plane())
  franka = scene.add_entity(
      gs.morphs.MJCF(file='xml/franka_emika_panda/panda.xml'),
  )
  scene.build()

  # Run simulation in a separate thread (required on macOS)
  gs.tools.run_in_another_thread(fn=run_sim, args=(scene, ))
  scene.viewer.start()


def run_sim(scene):
  i = 0
  while True:
    i += 1
    scene.step()
    if i > 200:
      break
  scene.viewer.stop()

if __name__ == "__main__":
  main()
