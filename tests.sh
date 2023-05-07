rm dot_files/*.dot dot_files/output/*.pdf
rm dot_files/bool_circ/*.dot dot_files/bool_circ/output/*.pdf
rm dot_files/bool_circ/transform/*.dot dot_files/bool_circ/transform/output/*.pdf
rm dot_files/bool_circ/evaluate/*.dot dot_files/bool_circ/evaluate/output/*.pdf
rm dot_files/bool_circ/simplify/*.dot dot_files/bool_circ/simplify/output/*.pdf
rm dot_files/bool_circ/hamming/*.dot dot_files/bool_circ/hamming/output/*.pdf
rm dot_files/open_digraph/*.dot dot_files/open_digraph/output/*.pdf
rm dot_files/random_graph/*.dot dot_files/random_graph/output/*.pdf

clear
for FILE in tests/* ; 
do python3 $FILE ;
echo "



" ; 
done