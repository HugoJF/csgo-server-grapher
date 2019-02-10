rrdtool graph sv1.png \
--imgformat PNG \
--title="Server Performance" \
--vertical-label "FPS" \
--start=n-61min \
--end=n-1min \
--color=BACK#CCCCCC \
--color=CANVAS#FEFEFE \
--color=SHADEB#9999CC \
--height=250 \
--upper-limit=120 \
--lower-limit=0 \
--grid-dash 0:1 \
--no-gridfit \
--watermark "Servidores de_nerdTV" \
--slope-mode \
DEF:sv1_fps=performance_143_202_39_221_27001.rrd:fps:AVERAGE \
DEF:sv1_var=performance_143_202_39_221_27001.rrd:var:AVERAGE \
DEF:sv1_players=performance_143_202_39_221_27001.rrd:players:AVERAGE \
LINE:sv1_fps#3634c0:STACK:"Server #1"

rm graphs/sv1.png
mv player_count.png graphs/sv1.png