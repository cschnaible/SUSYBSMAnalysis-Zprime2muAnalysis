#!/bin/bash

output_name=20190514

#python CompareAccEff.py -w our -o ${output_name}
#python CompareAccEff.py -w our -vr -o ${output_name}
#python CompareAccEff.py -w our -atZ -o ${output_name}
#python CompareAccEff.py -w our -vr -atZ -o ${output_name}
#python CompareAccEff.py -w ourZ  -o ${output_name}
#python CompareAccEff.py -w ourZ -vr -o ${output_name}
#python CompareAccEff.py -w ourZ -atZ -o ${output_name}
#python CompareAccEff.py -w ourZ -vr -atZ -o ${output_name}

python CompareMC.py -w our -o ${output_name}
#python CompareMC.py -w our -vr -o ${output_name}
#python CompareMC.py -w our -atZ -o ${output_name}
#python CompareMC.py -w our -vr -atZ -o ${output_name}
#python CompareMC.py -w ourZ  -o ${output_name}
#python CompareMC.py -w ourZ -vr -o ${output_name}
#python CompareMC.py -w ourZ -atZ -o ${output_name}
#python CompareMC.py -w ourZ -vr -atZ -o ${output_name}
