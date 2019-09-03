#!/bin/bash
for i in `seq 1 9`;
do
rrdtool graph graphs/sv$i.svg \
--imgformat SVG \
--title="Server #$i Performance" \
--vertical-label "FPS" \
--right-axis-label "Players" \
--right-axis 0.1:0 \
--start=n-1441min \
--end=n-1min \
--color=BACK#E5E3E0 \
--color=CANVAS#ffffff \
--height=300 \
--upper-limit=135 \
--lower-limit=0 \
--grid-dash 0:1 \
--watermark "Servidores de_nerdTV" \
--slope-mode \
DEF:sv1_fps=dbs/performance_177_54_150_15_2700$i.rrd:fps:AVERAGE \
DEF:sv1_players=dbs/performance_177_54_150_15_2700$i.rrd:players:AVERAGE \
DEF:sv1_ms=dbs/performance_177_54_150_15_2700$i.rrd:var:AVERAGE \
CDEF:sv1_players_scaled=sv1_players,10,* \
CDEF:sv1_ms_scaled=sv1_ms,10,* \
VDEF:sv1_fps_avg=sv1_fps,AVERAGE \
VDEF:sv1_players_avg=sv1_players,AVERAGE \
AREA:sv1_players_scaled#2C64A3:"Players\l" \
LINE:sv1_players_scaled#1f1c1e \
HRULE:128#222222aa:"128 TICK\l" \
HRULE:102#aaaaaaaa:"102.8 TICK\l" \
HRULE:78#000000ee:"7.8125ms\l" \
LINE2:sv1_fps#D42E25:"FPS\l" \
LINE1:sv1_ms_scaled#00FF00:"Frametime\l" \
GPRINT:sv1_fps_avg:"AVG\: %1.1lf%sFPS" \
GPRINT:sv1_players_avg:"PLAYER AVG\: %1.1lf%splayers\c"
done 


