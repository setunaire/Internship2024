# internship2024
This is my internship project at [Oddrun Co.](https://oddrun.ir/); It is a translation website with signup, login and logout options. It is deployed mainly using flask framework and [Google's madlad translation model](https://huggingface.co/google/madlad400-3b-mt).
MADLAD-400-3B-MT is a multilingual machine translation model based on the T5 architecture that was trained on 1 trillion tokens covering over 450 languages using publicly available data. It is competitive with models that are significantly larger.
Users can make accounts by entering their email address, username and password. These data are stored in a docker image of Postgres database. The python app was also dockerized; these two images are connected through docker compose.
Sincere thanks to DevOps engineers esp Javad Mirmoeini. I also thank @francescociulla who have helped me by his tutorials on youtube.

!!! This project may not be run on local server due to large size of dependencies. !!!
