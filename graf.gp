reset 
set terminal png font "Verdana"
set output "grafsk.png"

set title "Grafico Custo por Iteracao "
set xlabel "Iteration"
set ylabel "Cost"
unset key

plot "outsk.dat" u 1:2 w l 

set output "grafzt.png"

plot "outzt.dat" u 1:2 w l 
