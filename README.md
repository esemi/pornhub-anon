# Prototype of pornhub deanonimisation
---

## todo 
* ~split video to frames~
* ~detect faces~
* ~detect faces cascade~
* ~clustering same faces~
* crawl videos (need select source)
* collect faces DB (AWS Rekognition)

## todo optional
* crawl public faces DB
* filter open eyes only
* select best faces frame (RnD)
* compare our abd public DBs
* FindFace like service use for unknown persons


## links

* https://tjournal.ru/26824-polzovateli-dvacha-deanonimizirovali-rossiyskih-pornoaktris-s-pomoshchyu-findface
* https://nakedsecurity.sophos.com/2017/02/06/neural-face-recognition-network-tuned-with-650000-pornstar-images/
* https://nakedsecurity.sophos.com/2016/05/02/facial-recognition-used-to-strip-sex-workers-of-anonymity/
* https://camgirl.id/
* https://www.ambercutie.com/forums/threads/official-camgirl-id-acf-forum-thread.29006/


## Setup and usage

* sudo apt install redis python3.7 python-dev pkg-config 
* sudo pat install libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev libswresample-dev libavfilter-dev
* sudo apt install libopenblas-dev liblapack-dev build-essential cmake libx11-dev libgtk-3-dev

* fab -H pornanon@46.101.148.95 --prompt-for-login-password deploy
* ./app/task_loading.py 1000
* ./app/task_processing.py 1000

