from FWCore.PythonUtilities.LumiList import LumiList
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i','--input-json',dest='input_json',action='append',help='Input JSON files')
parser.add_argument('-o','--output-json',dest='output_json',default='json/combined.json',help='Output JSON file')
args = parser.parse_args()

outputJSON = LumiList(filename=args.input_json[0])
for jsonfile in args.input_json[1:]:
    thisJSON = LumiList(filename=jsonfile)
    outputJSON += thisJSON

if len(outputJSON.getDuplicates())>0:
    print 'Duplicates',outputJSON.getDuplicates()

outputJSON.writeJSON(args.output_json)

