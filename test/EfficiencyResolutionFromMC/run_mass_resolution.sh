#!/bin/bash

#############################
# vertex mass resolution
#############################

#python mass_resolution.py -y 2018 --syst-err 1.05 --var vertex_gen
#python mass_resolution.py -y 2017 --syst-err 1.05 --var vertex_gen
#python mass_resolution.py -y 2016 --syst-err 1.065 --var vertex_gen
#python mass_resolution.py -y 2018 --syst-err 1.05  --smear 1.15 --var vertex_gen
#python mass_resolution.py -y 2017 --syst-err 1.05  --smear 1.15 --var vertex_gen
#python mass_resolution.py -y 2016 --syst-err 1.065 --smear 1.15 --var vertex_gen

#############################
# Dilepton mass resolution
#############################

#python mass_resolution.py -y 2018 --syst-err 1.05  --var dil_mass_gen
#python mass_resolution.py -y 2017 --syst-err 1.05  --var dil_mass_gen
#python mass_resolution.py -y 2016 --syst-err 1.065 --var dil_mass_gen
#python mass_resolution.py -y 2018 --syst-err 1.05  --smear 1.15 --var dil_mass_gen
#python mass_resolution.py -y 2017 --syst-err 1.05  --smear 1.15 --var dil_mass_gen
#python mass_resolution.py -y 2016 --syst-err 1.065 --smear 1.15 --var dil_mass_gen

#############################
# vertex mass resolution wrt dilepton mass
#############################

#python mass_resolution.py -y 2018 --var dil_mass_vertex
#python mass_resolution.py -y 2017 --var dil_mass_vertex
#python mass_resolution.py -y 2016 --var dil_mass_vertex

#############################
# Generalized-Endpoint dilepton mass resolution
#############################

python mass_resolution.py -y 2018 --syst-err 1.05  --drell-yan powheg_GE --var dil_mass_GE_gen
#python mass_resolution.py -y 2017 --syst-err 1.05  --drell-yan powheg_GE --var dil_mass_GE_gen
#python mass_resolution.py -y 2016 --syst-err 1.065 --drell-yan powheg_GE --var dil_mass_GE_gen
#python mass_resolution.py -y 2018 --syst-err 1.05  --smear 1.15 --drell-yan powheg_GE --var dil_mass_GE_gen
#python mass_resolution.py -y 2017 --syst-err 1.05  --smear 1.15 --drell-yan powheg_GE --var dil_mass_GE_gen
#python mass_resolution.py -y 2016 --syst-err 1.065 --smear 1.15 --drell-yan powheg_GE --var dil_mass_GE_gen

