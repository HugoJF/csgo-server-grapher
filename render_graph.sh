#!/bin/bash
for i in `seq 1 9`;
do
rrdtool graph graphs/sv$i.png \
--imgformat PNG \
--title="Server #$i Performance" \
--vertical-label "FPS" \
--right-axis-label "Players" \
--right-axis 0.1:0 \
--start=n-61min \
--end=n-1min \
--color=BACK#CCCCCC \
--color=CANVAS#FEFEFE \
--color=SHADEB#9999CC \
--height=250 \
--upper-limit=135 \
--lower-limit=0 \
--grid-dash 0:1 \
--watermark "Servidores de_nerdTV" \
--slope-mode \
DEF:sv1_fps=dbs/performance_143_202_39_221_2700$i.rrd:fps:AVERAGE \
DEF:sv1_players=dbs/performance_143_202_39_221_2700$i.rrd:players:AVERAGE \
CDEF:sv1_players_scaled=sv1_players,10,* \
VDEF:sv1_fps_avg=sv1_fps,AVERAGE \
VDEF:sv1_players_avg=sv1_players,AVERAGE \
AREA:sv1_players_scaled#3634c066:"Players\l" \
LINE:sv1_players_scaled#333333 \
LINE2:sv1_fps#3634c0:"FPS\l" \
HRULE:128#00ff00:"128 TICK\l" \
HRULE:102#fff300:"102.8 TICK\l" \
GPRINT:sv1_fps_avg:"AVG\: %1.1lf%sFPS" \
GPRINT:sv1_players_avg:"PLAYER AVG\: %1.1lf%splayers\c"
done 


