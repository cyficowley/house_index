vlc -I dummy \
http://192.168.7.2:8081/ \
--video-filter=scene \
--vout=dummy \
--scene-format=jpg \
--scene-ratio=1 \
--scene-prefix=snapshot \
--scene-path=./frames/ \
vlc://quit

