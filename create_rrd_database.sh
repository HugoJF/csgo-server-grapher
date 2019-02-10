rrdtool create performance_143_202_39_221_27001.rrd --step 5 \
DS:fps:GAUGE:10:0:150 \
DS:var:GAUGE:10:0:30000 \
DS:players:GAUGE:10:0:20 \
RRA:AVERAGE:0.5:1:720 \
RRA:AVERAGE:0.5:12:3600
