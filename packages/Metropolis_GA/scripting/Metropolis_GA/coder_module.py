import os

import CodeAPI
import ProjectAPI

from iLock_SEIF import code_export

folder = "code"
filename = os.path.join(folder, ProjectAPI.Name + ".seif")
program_name = [p for p in CodeAPI.Programs][0].Name


if not os.path.exists(folder):
    os.makedirs(folder)
code_export.main(
    filename=filename,
    programNames=[program_name])
os.startfile(folder)
