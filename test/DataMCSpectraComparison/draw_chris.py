# Testing GIT
#!/usr/bin/env python

import sys, os, glob
from collections import defaultdict
from pprint import pprint
from optparse import OptionParser

# We have to optparse before ROOT does, or else it will eat our
# options (at least -h/--help gets eaten). So don't move this!
parser = OptionParser()
parser.add_option('-d', '--histo-dir', dest='histo_dir', default='data/DCSOnly',
                  help='Directory containing the input files for the data. Default is %default. The files expected to be in this directory are ana_datamc_data.root, the ROOT file containing the input histograms, and ana_datamc_data.lumi, the log file from the output of LumiCalc. Optionally the directory can contain a link to a directory for MC histogram ROOT files; the link/directory must be named "mc".')
parser.add_option('--no-print-table', action='store_false', dest='print_table', default=True,
                  help='Do not print out the ASCII table of event counts in specified mass ranges.')
parser.add_option('--no-save-plots', action='store_false', dest='save_plots', default=True,
                  help='Do not save the plots drawn.')
parser.add_option('--luminosity', dest='override_int_lumi', type='float',
                  help='Set the integrated luminosity manually (in 1/pb) rather than attempting to get it from the LumiCalc log file.')
parser.add_option('--no-lumi-rescale', action='store_false', dest='rescale_lumi', default=True,
                  help='Do not rescale the luminosity.')
parser.add_option('--for-rescale-factors', action='store_true', dest='for_rescale_factors', default=False,
                  help='Just print the tables for the Z peak counts to determine the luminosity rescaling factors (implies --no-lumi-rescale and --no-save-plots).')
parser.add_option('--lumi_syst_frac', dest='lumi_syst_frac', type='float', default=0.026,
                  help='Set the systematic uncertainty for the luminosity (as a relative value). Default is %default.')
parser.add_option('--no-draw-zprime', action='store_false', dest='draw_zprime', default=True,
                  help='Do not draw the Z\' curve.')
parser.add_option('--no-poisson-intervals', action='store_false', dest='use_poisson_intervals', default=True,
                  help='Do not use Poisson 68% CL intervals for the error bars on the data points.')
parser.add_option('--no-overflow-in-last-bin', action='store_false', dest='put_overflow_in_last_bin', default=True,
                  help='Do not add the overflow amount to the last bin.')
parser.add_option('--no-joins', action='store_false', dest='do_joins', default=True,
                  help='Do not lump together the MC contributions from different samples.')
parser.add_option('--no-join-ttbar', action='store_false', dest='join_ttbar_and_other_prompt_leptons', default=True,
                  help='Do not lump ttbar and other prompt leptons contributions together.')
parser.add_option('--join-dy-and-jets', action='store_true', dest='join_dy_and_jets', default=False,
                  help='Combine only Drell-Yan and jets samples.')
parser.add_option('--exclude-sample', action='append', dest='exclude_samples',
                  help='Specify a sample not to use (by name, e.g. wjets). To exclude more than one sample, give this option more than once.')
parser.add_option('--qcd-from-data', action='store_true', dest='qcd_from_data', default=False,
                  help='Replace MC predictions of QCD background by data-driven predictions.  External file qcd_from_data.root must be provided.')
parser.add_option('--include-quantity', action='append', dest='include_quantities',
                  help='If specified, will override the default list of quantities to compare in favor of the specified one. Specify this option more than once to use multiple quantities to compare.')
parser.add_option('--include-dilepton', action='append', dest='include_dileptons',
                  help='If specified, will override the default list of dileptons in favor of the specified one. Specify this option more than once to use multiple dileptons.')
parser.add_option('--include-cutset', action='append', dest='include_cutsets',
                  help='If specified, will override the default list of cutsets in favor of the specified one. Specify this option more than once to use multiple cutsets.')
parser.add_option('--include-massrange', action='append', dest='include_mass_ranges_for_table',
                  help='If specified, will override the default list of mass ranges for the ASCII table in favor of the specified one. Specify this option more than once to use multiple mass ranges.')
parser.add_option('--plot-dir-tag', action='store',dest='plot_dir_tag',default='test',
                  help='Adds argument to plot_dir path, useful for tagging the current version.')
parser.add_option('--plot-dir-base', action='store',dest='plot_dir_base',default='www_datamc',
                  help='Base directory to store plots')
parser.add_option('--plot-size', default='800,600',
                  help='The canvas size for drawing the plots.')
parser.add_option('--no-guess-yrange', action='store_false', dest='guess_yrange', default=True,
                  help='Do not try to guess out the y-axis range for plots, using instead the fixed values in the script.')
options, args = parser.parse_args()
#pprint(options) ; raise 1

# Done with option parsing, now can import things that import ROOT.

import SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples_chris as MCSamples
from SUSYBSMAnalysis.Zprime2muAnalysis.roottools_chris import cumulative_histogram, get_integral, move_below_into_bin, move_above_into_bin, plot_saver, poisson_intervalize, real_hist_max, real_hist_min, set_zp2mu_style, ROOT
from SUSYBSMAnalysis.Zprime2muAnalysis.hltTriggerMatch_cfi import overall_prescale

class Drawer:
    # Terminology:
    #
    # "cut set": the label for the set of cuts applied on the input
    # data. These correspond to substrings of the folder names in the
    # input file. E.g. "OurNewMuonsPlusMuonsMinus" folder -> "OurNew"
    # cut set.
    #
    # "join group": a set of MC samples that will be lumped together
    # in the plotted histograms (by color and in the legend) and in
    # the ASCII table.
    #
    # "nice-name": the string used for e.g. legend captions, usually
    # TLatex-ified. E.g. t#bar{t}.
    #
    # "sample name": the short name for the MC sample. For the sample
    # objects in MCSamples imported above, this is just
    # sample.name. E.g. zmumu.
    #
    # JMTBAD rest of it

    def __init__(self, options):
        self.histo_dir = options.histo_dir
        self.print_table = options.print_table
        self.save_plots = options.save_plots
        self.rescale_lumi = options.rescale_lumi
        self.lumi_syst_frac = options.lumi_syst_frac
        self.draw_zprime = options.draw_zprime
        self.use_poisson_intervals = options.use_poisson_intervals
        self.put_overflow_in_last_bin = options.put_overflow_in_last_bin
        self.do_joins = options.do_joins
        self.join_ttbar_and_other_prompt_leptons = options.join_ttbar_and_other_prompt_leptons
        self.join_dy_and_jets = options.join_dy_and_jets
        self.qcd_from_data = options.qcd_from_data
        self.guess_yrange = options.guess_yrange
        self.plot_dir_base = options.plot_dir_base
        self.plot_dir_tag = options.plot_dir_tag

        if not os.path.isdir(self.histo_dir):
            raise ValueError('histo_dir %s is not a directory' % self.histo_dir)

        #self.data_fn = os.path.join(self.histo_dir, 'ana_datamc_data.root')
        #self.data_fn = os.path.join(self.histo_dir, 'ana_datamc_data_Run2018_inc.root')
        self.data_fn = os.path.join(self.histo_dir, 'ana_datamc_Run2018ABCD_inc.root')
        if not os.path.isfile(self.data_fn):
            raise ValueError('data_fn %s is not a file' % self.data_fn)
        self.data_f = ROOT.TFile(self.data_fn)
        if not self.data_f.IsOpen() or self.data_f.IsZombie():
            raise ValueError('data_fn %s is not a ROOT file' % self.data_fn)
        
        # We look for a separate mc dir in our histo_dir first, for
        # the case where we want to use a specific set of MC files for
        # a given histo_dir. If none there, check if there is one
        # specified in options.  Else, use the general mc dir from the
        # current directory.
        self.mc_dir = os.path.join(self.histo_dir, 'mc')
        if not os.path.isdir(self.mc_dir):
            if hasattr(options, 'mc_dir'):
                self.mc_dir = options.mc_dir
            else:
                self.mc_dir = 'mc'
        if not os.path.isdir(self.mc_dir):
            raise ValueError('mc_dir %s is not a directory' % self.mc_dir)

        # If the options override the int_lumi, take that; otherwise
        # try to get the int_lumi from the file corresponding to
        # data_fn.
        if type(options.override_int_lumi) == float:
            self.int_lumi = options.override_int_lumi
        else:
            lumi_fn = self.data_fn.replace('.root', '.lumi')
            self.int_lumi = self.parse_lumi_from_log(lumi_fn)
            if self.int_lumi is None:
                raise ValueError('int_lumi could not be parsed from file %s' % lumi_fn)
        if self.int_lumi < 0:
            raise ValueError('int_lumi %f makes no sense' % self.int_lumi)

        # Use all samples specified in MCSamples that are not
        # requested to be dropped in the options. The sample objects
        # already-set values (like color, partial_weight) we won't
        # change, but the objects themselves may be modified. In
        # particular, we will use them as storage containers for
        # things like ROOT histograms and calculated things like scale
        # factors and event counts.
        self.samples = [s for s in MCSamples.samples if options.exclude_samples is None or s.name not in options.exclude_samples]
        self.hdata = None

        # Defaults for the dileptons, cutsets, and mass ranges for the
        # ASCII table.
        self.quantities_to_compare = ['DileptonMass', 'DimuonMassVertexConstrained']
        #self.dileptons = ['MuonsPlusMuonsMinus']
        self.dileptons = ['MuonsOppSign']
        self.cutsets = ['Our2018','Our2018MuPrescaled']#, 'Simple']
        self.mass_ranges_for_table = [(60,120),(120,),(120,200),(200,1000),(1000,2000),(2000,)]

        if options.include_quantities is not None:
            self.quantities_to_compare = options.include_quantities
        if options.include_dileptons is not None:
            self.dileptons = options.include_dileptons
        if options.include_cutsets is not None:
            self.cutsets = options.include_cutsets
        if options.include_mass_ranges_for_table is not None:
            self.mass_ranges_for_table = options.include_mass_ranges_for_table
        
        if options.for_rescale_factors:
            self.save_plots = False
            self.rescale_lumi = False
            self.mass_ranges_for_table = [(60,120)]
            #self.dileptons = ['MuonsPlusMuonsMinus']
            self.dileptons = ['MuonsOppSign']

        self.setup_root()
        self.plot_dir_base = os.path.join(self.plot_dir_base, self.plot_dir_tag)
        os.system('mkdir -p %s' % self.plot_dir_base)
        width,height = options.plot_size.split(',')
        self.ps = plot_saver(self.plot_dir_base, size=(int(width), int(height)), pdf_log=True, pdf=True)

        self.table_sections = []
        self.table_rows = []
        
    def setup_root(self):
        set_zp2mu_style()
        ROOT.gStyle.SetPadTopMargin(0.09)
        ROOT.gStyle.SetPadBottomMargin(0.12)
        ROOT.gStyle.SetPadLeftMargin(0.10)
        ROOT.gStyle.SetPadRightMargin(0.05)
        ROOT.TH1.AddDirectory(False)
        
    def get_join(self, sample_name):
        # If we're to merge the sample given with other histograms,
        # return a new nice-name and color for the sum. Otherwise,
        # return None.

        if self.do_joins:
            if 'qcd' in sample_name or sample_name in ('inclmu15', 'wmunu', 'wjets'):
                return 'jets', ROOT.kOrange+1
            if 'dy' in sample_name or sample_name == 'zmumu':
                return '#gamma/Z #rightarrow #mu^{+}#mu^{-}', ROOT.kAzure+1
            if ('tW' in sample_name or 'tbarW' in sample_name):
                return 'single top', ROOT.kViolet+1
            if ('WW' in sample_name or 'WZ' in sample_name or 'ZZ' in sample_name):
                return 'diboson',ROOT.kGreen+1
            if ('ttbar' in sample_name):
                return 't#bar{t}',ROOT.kRed-4
            if ('Wjets' in sample_name):
                return 'jets',ROOT.kOrange+1
#            if not self.join_dy_and_jets:
#                if self.join_ttbar_and_other_prompt_leptons and sample_name in ('ttbar', 'ttbar_powheg', 'tW', 'tbarW', 'ztautau', 'ww', 'wz', 'zz'):
#                    return 't#bar{t} + other prompt leptons', 2
#                elif not self.join_ttbar_and_other_prompt_leptons and sample_name in ('tW', 'tbarW', 'ztautau', 'ww', 'wz', 'zz'):
#                    return 'other prompt leptons', 2
#            else:
#                if ('tW' in sample_name or 'tbarW' in sample_name):
#                    return 'single top', 1
#                elif sample_name in ('ww'):
#                    return 'WW', 3

        return None, None

    def is_join(self, sample_name):
        return self.get_join(sample_name)[0] is not None
    
    def get_join_name(self, sample_name):
        return self.get_join(sample_name)[0]

    def get_join_color(self, sample_name):
        return self.get_join(sample_name)[1]

    def get_color(self, sample):
        color = self.get_join_color(sample.name)
        return sample.color if color is None else color

    def get_rebin_factor(self, dilepton, cutset, quantity_to_compare):
        # For the combination of the arguments, figure out by which
        # factor to rebin the input histograms. E.g. for DileptonMass
        # the input is currently 1-GeV bins; here we change this to
        # 10-GeV bins.
        if 'Mass' in quantity_to_compare: return 1
        if dilepton == 'MuonsSameSign':
            if quantity_to_compare == 'DileptonMass':
                return 5
        if cutset=='Our2018':
            if 'DimuonMassVertexConstrained' in quantity_to_compare:
                return 20
            if 'DileptonMass' in quantity_to_compare:
                return 20
            if 'Log' in quantity_to_compare:
                return 10
        if 'Prescaled' in cutset:
            if True:
                if 'DimuonMassVertexConstrained' in quantity_to_compare:
                    return 20
                if 'DileptonMass' in quantity_to_compare:
                    return 20
                if 'Log' in quantity_to_compare:
                    return 10
            else:
                if 'DimuonMassVertexConstrained' in quantity_to_compare:
                    return 2
                if 'DileptonMass' in quantity_to_compare:
                    return 2
                if 'Log' in quantity_to_compare:
                    return 2
        if quantity_to_compare in ['DileptonPt','DileptonPz','LeptonPt','LeptonPz','LeptonP']:
            return 10
        if quantity_to_compare in ['RelCombIso', 'RelIsoSumPt']:
            return 1
        if quantity_to_compare in ['DileptonPhi', 'DileptonRap', 'LeptonPhi', 'LeptonEta']:
            return 1
        return 1
        
    def rebin_histogram(self, h, cutset, dilepton, quantity_to_compare):
        # JMTBAD Make this more flexible to do arbitrary binning, e.g. by
        # mass resolution.
        ndim = h.GetDimension()
        if ndim == 1:
            h.Rebin(self.get_rebin_factor(dilepton, cutset, quantity_to_compare))
        elif ndim == 2:
            h.Rebin2D(self.get_rebin_factor(dilepton, cutset, quantity_to_compare))

    def divide_bin_width(self,h):
        '''Need to do this by hand since I want to allow for
        variable bin widths'''
        nbins = h.GetNbinsX()
        for i in range(1,nbins+1):
            c = h.GetBinContent(i)
            e = h.GetBinError(i)
            w = h.GetXaxis().GetBinUpEdge(i) - h.GetXaxis().GetBinLowEdge(i)
            h.SetBinContent(i,c/w)
            h.SetBinError(i,e/w)

    def get_x_axis_range(self, cutset, dilepton, quantity_to_compare):
        # For the given combination of the arguments, return the
        # desired restriction on the viewable x-axis range, if
        # any. E.g. for DileptonMass, only show from 60-2000 GeV on
        # the displayed plot.
        if dilepton == 'MuonsSameSign':
            if quantity_to_compare == 'DileptonPt':
                return 0,350
            if quantity_to_compare == 'DileptonRap':
                return -3,3
            if quantity_to_compare == 'LeptonPt':
                return 0,300
        if quantity_to_compare == 'RelCombIso':
            return 0,0.55
        if quantity_to_compare == 'RelIsoSumPt':
            return 0,0.1
        if quantity_to_compare == 'IsoSumPt':
            return 0,50
        if 'Electron' in dilepton:
            return 100, 1000
        if 'MuonsSameSign' in dilepton:
            if quantity_to_compare in ['DileptonMass', 'DimuonMassVertexConstrained']:
                return 50, 1000
        if cutset=='Our2018':
            if quantity_to_compare in [\
                    'DileptonMass', 'DimuonMassVertexConstrained',\
                    'DileptonMass_bb', 'DimuonMassVertexConstrained_bb',\
                    'DileptonMass_be', 'DimuonMassVertexConstrained_be',\
                    'DileptonMass_ee', 'DimuonMassVertexConstrained_ee',\
                    ]: return 50, 3500
            if quantity_to_compare in [\
                    'DimuonMassVtxConstrainedLog','DimuonMassVtxConstrainedLog_bb',\
                    'DimuonMassVtxConstrainedLog_be','DimuonMassVtxConstrainedLog_ee'
                    ]: return 50, 3500
        if 'Prescaled' in cutset:
            if quantity_to_compare in [\
                    'DileptonMass', 'DimuonMassVertexConstrained',\
                    'DileptonMass_bb', 'DimuonMassVertexConstrained_bb',\
                    'DileptonMass_be', 'DimuonMassVertexConstrained_be',\
                    'DileptonMass_ee', 'DimuonMassVertexConstrained_ee',\
                    'DimuonMassVtxConstrainedLog','DimuonMassVtxConstrainedLog_bb',\
                    'DimuonMassVtxConstrainedLog_be','DimuonMassVtxConstrainedLog_ee'
                    #]: return 60, 120
                    ]: return 50, 3500
        if quantity_to_compare in ['LeptonPt']:
            return 0, 2000
        if quantity_to_compare in ['DileptonPt']:
            return 0, 1500
        if quantity_to_compare in ['DileptonPz']:
            return 0, 2500
        if quantity_to_compare == 'LeptonEta':
            return -2.5,2.5
        if quantity_to_compare == 'DileptonRap':
            return -3.,3.
        return None

    def get_log_x(self, cutset, dilepton, quantity_to_compare):
        return 'Log' in quantity_to_compare

    def parse_lumi_from_log(self, log_fn):
        # JMTBAD magic, fragile parsing
        lumi_scale = 1 # assume /pb
        this = False
        for line in open(log_fn):
            if this:
                x = float(line.split()[-2])
                return x*lumi_scale
            if line == '---------------------------------------------------------------\n':
                this = True
            # lumi returned is expected to be in /pb; try to determine units from log file
            if 'Recorded' in line and 'Run' not in line:
                if '/fb' in line:
                    lumi_scale = 1000
                elif '/pb' not in line:
                    raise ValueError('cannot determine units from lumi log file: neither /fb nor /pb strings found')

    def get_lumi_rescale_factor(self, cutset, dilepton, cat):
        # Get the cut set dependent factor by which we rescale the
        # luminosity.


        # If we're instructed not to rescale at all, don't.
        if not self.rescale_lumi:
            return 1.

        # Don't rescale e-mu plots. 
        if 'Electron' in dilepton:
            return 1.

        # These numbers are specified manually here, transcribing from
        # the 60-120 GeV tables from the prescaled path that are
        # produced when running this script with rescaling turned off,
        # rather than trying to be smart and getting them from the
        # histogram files.
        # Factors below were calculated for the MuonPhys JSON file for
        # all 2012 collision runs released on December 14 and
        # correspond to 20.637/fb.
        # If the cutset is not one of the below, don't rescale.
        if 'Prescaled' in cutset:
            return 1.
        rescale_factor = 1.
        if 'New' in cutset:
           # rescale_factor = 21671./22531.7
            rescale_factor = 1
        elif '2012' in cutset or cutset =='OurNoIso':
            rescale_factor = 1
           # rescale_factor = 24502./24610.4

        elif '2018' in cutset:
            if cat=='bb':
               rescale_factor = 28430.0/30977.464924
            elif cat=='be':
               rescale_factor = 42349.0/46402.539916
            elif cat=='':
               rescale_factor = 70779.0/77380.003337

        return rescale_factor

    def advertise_lines(self,cat):
        s = []
        s.append('total lumi from data: %.f/pb' % self.int_lumi)
        s.append('rescaling mumu MC histograms by these cut-dependent factors:')
        for cutset in self.cutsets:
            s.append('%18s:%.10f' % (cutset, self.get_lumi_rescale_factor(cutset, '',cat)))
        s.append('"joins" are:')
        for sample in self.samples:
            s.append('%10s -> %s' % (sample.name, self.get_join_name(sample.name)))
        return s

    def subtitleize(self, dilepton):
        return {
            'MuonsPlusMuonsMinus': '#mu^{+}#mu^{-}',
            'MuonsOppSign': '#mu^{+}#mu^{-}',
            'MuonsPlusMuonsPlus':  '#mu^{+}#mu^{+}',
            'MuonsMinusMuonsMinus': '#mu^{-}#mu^{-}',
            'MuonsSameSign': '#mu^{#pm}#mu^{#pm}',
            'MuonsAllSigns': '#mu#mu',
            'ElectronsPlusElectronsMinus': 'e^{+}e^{-}',
            'ElectronsPlusElectronsPlus': 'e^{+}e^{+}',
            'ElectronsMinusElectronsMinus': 'e^{-}e^{-}',
            'ElectronsSameSign': 'e^{#pm}e^{#pm}',
            'ElectronsAllSigns': 'ee',
            'MuonsPlusElectronsMinus': '#mu^{+}e^{-}',
            'MuonsMinusElectronsPlus': '#mu^{-}e^{+}',
            'MuonsPlusElectronsPlus': '#mu^{+}e^{+}',
            'MuonsMinusElectronsMinus': '#mu^{-}e^{-}',
            'MuonsElectronsOppSign': '#mu^{+}e^{-}/#mu^{-}e^{+}',
            'MuonsElectronsSameSign': '#mu^{#pm}e^{#pm}',
            'MuonsElectronsAllSigns': 'e#mu',
            }[dilepton]

    def titleize(self, quantity_to_compare):
        return {
            'DileptonMass': 'm(%s)%s',
            'DileptonMass_bb': 'm(%s)%s',
            'DileptonMass_be': 'm(%s)%s',
            'DimuonMassVertexConstrained': 'm(%s)%s',
            'DimuonMassVertexConstrained_bb': 'm(%s)%s',
            'DimuonMassVertexConstrained_be': 'm(%s)%s',
            'DimuonMassVtxConstrainedLog': 'm(%s)%s',
            'DimuonMassVtxConstrainedLog_bb': 'm(%s)%s',
            'DimuonMassVtxConstrainedLog_be': 'm(%s)%s',
            'DileptonPt': '%s p_{T}%s',
            'DileptonPz': '%s p_{z}%s',
            'DileptonRap': '%s rapidity%s',
            'LeptonPt': "%s leptons p_{T}%s",
            'LeptonPz': "%s leptons p_{z}%s",
            'LeptonEta': "%s leptons #eta%s",
            'RelIsoSumPt': "%s leptons relative tk. iso.%s",
            'IsoSumPt': "%s leptons tk. iso. sum%s",
            'RelCombIso': "%s leptons relative comb. iso.%s",
            }.get(quantity_to_compare, quantity_to_compare + ', %s, %s')

    def unitize(self, quantity_to_compare):
        return {
            'DileptonMass': ' [GeV]',
            'DileptonMass_bb': ' [GeV]',
            'DileptonMass_be': ' [GeV]',
            'DimuonMassVertexConstrained': ' [GeV]',
            'DimuonMassVertexConstrained_bb': ' [GeV]',
            'DimuonMassVertexConstrained_be': ' [GeV]',
            'DimuonMassVtxConstrainedLog': ' [GeV]',
            'DimuonMassVtxConstrainedLog_bb': ' [GeV]',
            'DimuonMassVtxConstrainedLog_be': ' [GeV]',
            'DileptonPt': ' [GeV]',
            'DileptonPz': ' [GeV]',
            'LeptonPt': ' [GeV]',
            'LeptonPz': ' [GeV]',
            'LeptonEta': '',
            'LeptonPhi': ' [rad]',
            'DileptonPhi': ' [rad]',
            'DileptonRap': '',
            'RelCombIso': '',
            'RelIsoSumPt': '',
            'IsoSumPt': ' [GeV]',
            }.get(quantity_to_compare, ' [XXX]')

    def get_dir_name(self, cutset, dilepton):
        return cutset + dilepton + 'Histos'

    def get_y_axis_range(self, dilepton, cumulative):
        return None

    def handle_overflows(self, h, range):
        if h.GetDimension() != 1:
            return
        if not self.put_overflow_in_last_bin:
            return
        if range is None:
            range = h.GetBinLowEdge(1), h.GetBinLowEdge(h.GetNbinsX()+1)
        move_above_into_bin(h, range[1])

    def get_sum_weights(self,f):
        weights = getattr(f,'EventCounter').Get('weights')
        return weights.GetBinContent(2)-weights.GetBinContent(1)

    def prepare_mc_histograms(self, cutset, dilepton, quantity_to_compare, cumulative, bin_width, cat):
        # For each sample in the list of MC samples, we get the
        # specified histogram from the appropriate input file, clone
        # it, rebin/scale/otherwise manipulate it as necessary, and
        # store the result as The Histogram in the sample object.
        for sample in self.samples:
            if (self.qcd_from_data and 'MuPrescaled' not in cutset and 'Electron' not in dilepton and sample.name == 'inclmu15' and quantity_to_compare in ['DileptonMass', 'DimuonMassVertexConstrained', 'DimuonMassVtxConstrainedLog']):
                # Replace QCD MC prediction by that obtained from data.
                mc_fn = os.path.join('./', 'qcd_from_data.root')
                f = ROOT.TFile(mc_fn)
                if 'MuonsSameSign' in dilepton:
                    sample.histogram = f.Get('ss').Clone()
                elif 'MuonsPlusMuonsMinus' in dilepton or 'MuonsOppSign' in dilepton:
                    sample.histogram = f.Get('os').Clone()
                elif 'MuonsAllSigns' in dilepton:
                    sample.histogram = f.Get('ss').Clone()
                    sample.histogram.Add(f.Get('os'), 1.)
                else:
                    print "+++ Unknown dilepton type! +++"

                # All this mess is just to copy/paste the content of the histogram in [50; 2000] GeV range into the histogram in [0; 3000] GeV range
                nbins = sample.histogram.GetNbinsX();
                # for ibin in range(1, nbins+1):
                #     xlow = sample.histogram.GetBinLowEdge(ibin)
                #     xupp = xlow + sample.histogram.GetBinWidth(ibin)
                #     print ibin, xlow, xupp, sample.histogram.GetBinContent(ibin)
                xlow = int(sample.histogram.GetBinLowEdge(1))
                xupp = int(sample.histogram.GetBinLowEdge(nbins) + sample.histogram.GetBinWidth(1))
                extended_hist = ROOT.TH1F("", "ss", 3000, 0, 3000)
                for ibin in range(1, 3001):
                    if ibin < xlow or ibin > xupp:
                        extended_hist.SetBinContent(ibin, 0)
                        extended_hist.SetBinError(ibin, 0)
                    else:
                        jbin = ibin-xlow
                        extended_hist.SetBinContent(ibin, sample.histogram.GetBinContent(jbin))
                        extended_hist.SetBinError(ibin, sample.histogram.GetBinError(jbin))
                #    print ibin, extended_hist.GetBinLowEdge(ibin), extended_hist.GetBinContent(ibin)
                # Use old QCD temporarily
                #sample.histogram = extended_hist.Clone()

                if (quantity_to_compare == 'DimuonMassVtxConstrainedLog'):
                    # Re-pack fixed-bin-width histogram into a variable-bin-width one
                    mc_fn = os.path.join(self.mc_dir, 'ana_datamc_%s.root' % sample.name)
                    f = ROOT.TFile(mc_fn)
                    varbin_histogram = getattr(f, self.get_dir_name(cutset, dilepton)).Get(quantity_to_compare).Clone()

                    nbins_var = varbin_histogram.GetNbinsX()
                    nbins_fix = sample.histogram.GetNbinsX()
                    for ibin_var in range(1, nbins_var+1):
                        xlow_var = varbin_histogram.GetBinLowEdge(ibin_var)
                        xupp_var = xlow_var + varbin_histogram.GetBinWidth(ibin_var)
                        # print ibin_var, xlow_var, xupp_var
                        cbin = 0
                        for ibin_fix in range(1, nbins_fix+1):
                            bin_center = sample.histogram.GetBinCenter(ibin_fix)
                            if (bin_center > xlow_var and bin_center < xupp_var):
                                # print "     ", ibin_fix, bin_center, sample.histogram.GetBinContent(ibin_fix)
                                cbin = cbin + sample.histogram.GetBinContent(ibin_fix)
                        # print "  ", ibin_var, cbin
                        varbin_histogram.SetBinContent(ibin_var, cbin)

                    sample.histogram = varbin_histogram.Clone()
                    sample.histogram.GetXaxis().SetMoreLogLabels(True)

                sample.scaled_by = 1. # Assume that the histogram is appropriately normalized.
            else:
                mc_fn = os.path.join(self.mc_dir, 'ana_datamc_%s.root' % sample.name)
                f = ROOT.TFile(mc_fn)
                sample.histogram = getattr(f, self.get_dir_name(cutset, dilepton)).Get(quantity_to_compare).Clone()
                #sample.scaled_by = self.int_lumi * self.get_lumi_rescale_factor(cutset, dilepton, cat) * sample.partial_weight_eff
                sumofweights = self.get_sum_weights(f)
                sample.scaled_by = self.int_lumi * self.get_lumi_rescale_factor(cutset, dilepton, cat) * sample.cross_section / sumofweights
                if 'MuPrescaled' in cutset and 'NoCommon' not in cutset:
                    sample.scaled_by = sample.scaled_by / overall_prescale

            # Assume that the QCD histogram includes W+jets as well.
            if (self.qcd_from_data and 'MuPrescaled' not in cutset and 'Electron' not in dilepton and sample.name in ('wmunu', 'wjets') and quantity_to_compare in ['DileptonMass', 'DimuonMassVertexConstrained', 'DimuonMassVtxConstrainedLog']):
                nbins = sample.histogram.GetNbinsX()
                for ibin in range(1, nbins+1):
                    sample.histogram.SetBinContent(ibin, 0.)
                    sample.histogram.SetBinError(ibin, 0.)

            self.rebin_histogram(sample.histogram, cutset, dilepton, quantity_to_compare)
            if bin_width and not cumulative: 
                self.divide_bin_width(sample.histogram)
            sample.histogram.Scale(sample.scaled_by)

            if cumulative and not bin_width:
                sample.histogram = cumulative_histogram(sample.histogram)
            else:
                self.handle_overflows(sample.histogram, self.get_x_axis_range(cutset, dilepton, quantity_to_compare))

            sample.histogram.SetMarkerStyle(0)
            color = self.get_color(sample)
            sample.histogram.SetLineColor(color)
            if not sample.is_zprime:
                sample.histogram.SetFillColor(color)
            if 'Log' in quantity_to_compare: sample.histogram.GetXaxis().SetMoreLogLabels(True)

    def prepare_data_histogram(self, cutset, dilepton, quantity_to_compare, cumulative, bin_width, cat):
        self.hdata = getattr(self.data_f, self.get_dir_name(cutset, dilepton)).Get(quantity_to_compare).Clone()
        self.rebin_histogram(self.hdata, cutset, dilepton, quantity_to_compare)
        range = self.get_x_axis_range(cutset, dilepton, quantity_to_compare)

        if cumulative and not bin_width:
            self.hdata = cumulative_histogram(self.hdata)
        else:
            self.handle_overflows(self.hdata, range)
        if 'Log' in quantity_to_compare: self.hdata.GetXaxis().SetMoreLogLabels(True)

        # if not self.put_overflow_in_last_bin:
            # Not so important if the MC histograms have entries past
            # the view range that isn't shown, but not so for
            # data. Check that there's no data off screen.
            # overflow_integral = get_integral(self.hdata, range[1], integral_only=True)
            # if overflow_integral > 0:
            #    raise ValueError('WARNING: in %s, data histogram has points in overflow (mass bins above %.f GeV)! integral = %f' % (cutset + dilepton, range[1], overflow_integral))

    def make_table(self, cutset, dilepton,quantity_to_compare):
        # Make a nicely formatted ASCII table of event counts in the
        # specified mass ranges, along with uncertainties.
        for mass_range in self.mass_ranges_for_table:
            self.table_sections.append((cutset, dilepton, mass_range))
            
            self.table_rows.append('*'*(50+20*9) + '\n\n')
            self.table_rows.append('ANCHORMEcuts: %s  dilepton: %s  mass range: %s\n' % (cutset, dilepton, mass_range))

            # For all the MC samples, calculate the integrals over the
            # current mass range and store it in the sample object.
            for sample in self.samples:
                sample.integral = get_integral(sample.histogram, *mass_range, integral_only=True, include_last_bin=False)
                sample.raw_integral = sample.integral / sample.scaled_by

            # Header. (I hope you have a widescreen monitor, a small font, and good eyes.)
            self.table_rows.append('%50s%20s%20s%20s%20s%20s%20s%20s%20s%20s\n' % ('sample', 'weight', 'raw integral', 'integral', 'stat error', 'limit if int=0', 'syst error', 'syst(+)stat', 'lumi error', 'total'))

            # Print the row for the event count from the data (only
            # the integral and statistical uncertainty columns will be
            # filled).
            data_integral = get_integral(self.hdata, *mass_range, integral_only=True, include_last_bin=False)
            self.table_rows.append('%50s%20s%20i%20.6f%20.6f\n' % ('data', '-', int(data_integral), data_integral, data_integral**0.5))

            # As we loop over the MC samples, keep some running sums
            # of integrals and variances. Do one such set including
            # the whole MC, and a set for each join group.
            sum_mc = 0.
            var_sum_mc = 0.
            syst_var_sum_mc = 0.
            sums = defaultdict(float) # will initialize to 0. on first lookup
            var_sums = defaultdict(float)
            syst_var_sums = defaultdict(float)

            # Loop over the MC samples in order of decreasing
            # integral.
            for sample in sorted(self.samples, key=lambda x: x.integral, reverse=True):
                # Calculate the contributions to the variances for the
                # statistical and systematic uncertainties for this
                # sample.
                w = sample.scaled_by
                if sample.integral < 0:
                    print sample.name, mass_range, sample.integral, w
                    sample.integral = 0
                var = w * sample.integral # not w**2 * sample.integral because sample.integral is already I*w
                syst_var = (sample.syst_frac * sample.integral)**2

                # Add the integral and the variances to the whole-MC
                # values, if it is to be included (i.e. don't include
                # Z' samples).
                if not sample.is_zprime:
                    sum_mc += sample.integral
                    var_sum_mc += var
                    syst_var_sum_mc += syst_var

                # If this sample belongs to a join group, add the
                # integral and the variances to the values for the
                # join group.
                join_name = self.get_join_name(sample.name)
                if join_name is not None:
                    sums[join_name] += sample.integral
                    var_sums[join_name] += var
                    syst_var_sums[join_name] += syst_var

                # For integrals that turn out to be zero due to not
                # enough statistics, we will give also the 95% CL
                # upper limit.
                limit = '%.6f' % (3*w) if sample.integral == 0 else '-'

                # For this sample alone, determine the combined
                # statistical+systematic uncertainty, the uncertainty
                # due to luminosity, and the total of all three.
                syst_plus_stat = (var + syst_var)**0.5
                lumi_err = self.lumi_syst_frac * sample.integral
                tot_err = (var + syst_var + lumi_err**2)**0.5

                # Print this row of the table.
                self.table_rows.append('%50s%20.6f%20f%20.6f%20.6f%20s%20.6f%20.6f%20.6f%20.6f\n' % (sample.nice_name, w, sample.raw_integral, sample.integral, var**0.5, limit, syst_var**0.5, syst_plus_stat, lumi_err, tot_err))

            self.table_rows.append('-'*(50+20*9) + '\n')
            
            # Determine the uncertainties and print the rows for each
            # of the join groups. Sort this section by decreasing integral.
            join_integrals = sums.items()
            join_integrals.sort(key=lambda x: x[1])
            for join_name, join_integral in join_integrals:
                lumi_err = self.lumi_syst_frac * sums[join_name]
                syst_plus_stat = (var_sums[join_name] + syst_var_sums[join_name])**0.5
                tot_err = (var_sums[join_name] + syst_var_sums[join_name] + lumi_err**2)**0.5
                self.table_rows.append('%50s%20s%20s%20.6f%20.6f%20s%20.6f%20.6f%20.6f%20.6f\n' % (join_name, '-', '-', sums[join_name], var_sums[join_name]**0.5, '-', syst_var_sums[join_name]**0.5, syst_plus_stat, lumi_err, tot_err))

            self.table_rows.append('-'*(50+20*9) + '\n')

            # For the sum of all MC, determine the combined
            # statistical+systematic uncertainty, the uncertainty due
            # to luminosity, and the total of all three. Then print
            # the whole-MC row.
            syst_plus_stat = (var_sum_mc + syst_var_sum_mc)**0.5
            lumi_err = self.lumi_syst_frac * sum_mc
            tot_err = (var_sum_mc + syst_var_sum_mc + lumi_err**2)**0.5
            self.table_rows.append('%50s%20s%20s%20.6f%20.6f%20s%20.6f%20.6f%20.6f%20.6f\n' % ('sum MC (not including Z\')', '-', '-', sum_mc, var_sum_mc**0.5, '-', syst_var_sum_mc**0.5, syst_plus_stat, lumi_err, tot_err))

            self.table_rows.append('\n')
        self.table_rows.append('\n')

    def should_draw_zprime(self, dilepton):
        return self.draw_zprime and dilepton == 'MuonsPlusMuonsMinus'

    def get_zprime_histogram(self):
        # JMTBAD Extend to the rest of the Z' samples when there are any.
        try:
            from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import zssm1000
            return zssm1000.histogram        # Loaded/scaled already in prepare_mc_histograms since the loop over the samples list modified the original object that zssm1000 points to.
        except ImportError:
            pass

    def draw_legend(self, dilepton, cumulative, log_x):
        # Legend placement coordinates and sizes depend on factors set
        # elsewhere, too, so this is fragile.
        #if dilepton == 'MuonsPlusMuonsMinus' and cumulative:
        if dilepton == 'MuonsOppSign' and cumulative:
            legend = ROOT.TLegend(0.70, 0.69, 0.86, 0.88)
        elif log_x:
            legend = ROOT.TLegend(0.70, 0.55, 0.86, 0.88)
        else:
            if self.join_dy_and_jets:
                legend = ROOT.TLegend(0.60, 0.50, 0.86, 0.88)
            else:
                legend = ROOT.TLegend(0.60, 0.69, 0.86, 0.88)
                #legend = ROOT.TLegend(0.60, 0.60, 0.86, 0.88)

        legend.SetFillColor(0)
        legend.SetBorderSize(0)

        # Add an entry for the data points.
        entry = legend.AddEntry('data_marker', 'Data', 'EP')
        entry.SetMarkerStyle(20)
        entry.SetMarkerSize(0.8)
        entry.SetMarkerColor(ROOT.kBlack)

        # Add entries for the MC samples to the legend, respecting
        # join groups (i.e. don't add the same nice-name twice).
        legend_already = set()
        for sample in reversed(self.samples):
            if sample.is_zprime and not self.should_draw_zprime(dilepton):
                continue

            nice_name = sample.nice_name

            join_name = self.get_join_name(sample.name)
            if join_name is not None:
                if join_name in legend_already:
                    continue
                else:
                    legend_already.add(join_name)
                    nice_name = join_name
            legend.AddEntry(sample.histogram, nice_name, 'F') # Gets the color and fill style from the histogram.

        legend.SetTextSize(0.03)
        legend.Draw('same')

        return legend

    def draw_data_on_mc(self, cutset, dilepton, quantity_to_compare, cumulative, bin_width):
        # Make a Stack for the MC histograms. We draw it first so the
        # data points will be drawn on top later.  We assume that in
        # the list of samples, the join groups are contiguous already
        # so that like-colored histograms will be next to each other.
        
        s = ROOT.THStack('s', '')
        for sample in self.samples:
            # Don't stack the Z' samples.
            if sample.is_zprime:
                continue
            s.Add(sample.histogram) # Assumes they've already been prepared.

        # Figure out its titles.
        xtitle = self.titleize(quantity_to_compare) % (self.subtitleize(dilepton), self.unitize(quantity_to_compare))
        if cumulative and not bin_width:
            # E.g. Events >= m(mu+mu-).
            ytitle = 'Events #geq %s' % (self.titleize(quantity_to_compare) % (self.subtitleize(dilepton), ''))
        else:
            # E.g. Events/5 GeV.
            if bin_width:
                ytitle = 'Events / %s'%self.unitize(quantity_to_compare).translate(None,'()[]').strip()
            else:
                ytitle = 'Events / %i%s' % (self.get_rebin_factor(dilepton, cutset, quantity_to_compare), self.unitize(quantity_to_compare).translate(None, '()[]')) # Events/5 GeV. JMTBAD assumes original histogram had 1 GeV bins and was rebinned simply -- ignores rebin_histogram ability to have arb. bins
                if quantity_to_compare == 'DileptonRap':
                    ytitle = 'Events / 0.5'
                elif quantity_to_compare == 'RelIsoSumPt':
                    ytitle = 'Events / 0.02'
                elif quantity_to_compare == 'RelCombIso':
                    ytitle = 'Events / 0.05'
                elif 'Log' in quantity_to_compare:
                    ytitle = 'Events / bin'
        s.SetTitle(';%s;%s' % (xtitle, ytitle))

        s.Draw('hist')

        # Must call Draw first or the THStack doesn't have a histogram/axes.
        s.GetXaxis().SetTitleOffset(1.1)
        s.GetXaxis().SetTitleSize(0.05)
        if 'MuonsSameSign' in dilepton:
            s.GetYaxis().SetTitleOffset(0.9)
        else:
            s.GetYaxis().SetTitleOffset(0.9)
        s.GetYaxis().SetTitleSize(0.047)
        if 'Log' in quantity_to_compare: s.GetXaxis().SetMoreLogLabels()

        # Set the x-axis range as specified. Then determine what
        # the real extrema of the data histogram and the MC stack are
        # over the xrange specified.
        xrange = self.get_x_axis_range(cutset, dilepton, quantity_to_compare)
        mymin, mymax = None, None
        if xrange is not None:
            s.GetXaxis().SetRangeUser(*xrange)
            self.hdata.GetXaxis().SetRangeUser(*xrange)
            mymin = real_hist_min(s.GetStack().Last(), user_range=xrange)
            mymax = real_hist_max(s.GetStack().Last(), user_range=xrange, use_error_bars=False)
            #mymin = s.GetMinimum()
            #mymax = s.GetMaximum()
            # Minimum of data will be zero so don't use it to set the y-axis range minimum
            if self.hdata.GetEntries() > 0:
                if bin_width: 
                    hdata = self.hdata.Clone()
                    self.divide_bin_width(hdata)
                    rhmax = real_hist_max(hdata, user_range=xrange)
                    mymax = max(mymax, rhmax)
                else:
                    rhmax = real_hist_max(self.hdata, user_range=xrange)
                    mymax = max(mymax, rhmax)

        #if self.guess_yrange:
        #    mymin = real_hist_min(self.hdata, user_range=xrange)
        #    mymax = real_hist_max(self.hdata, user_range=xrange)

        # Can override the above fussing.
        #yrange = self.get_y_axis_range(dilepton, cumulative)
        #if yrange is not None:
        #    if yrange[0] is not None:
        #        mymin = yrange[0]
        #    if yrange[1] is not None:
        #        mymax = yrange[1]

        #mymin = 0.05
    
        mymin = mymin*0.1
        mymax = mymax*1.05
        if mymin is not None: s.SetMinimum(mymin)
        if mymax is not None: s.SetMaximum(mymax)

        # Calculate (data-bckg)/bckg.  Do it before TH1 gets converted
        # to TGraphAsymmErrors by poisson_intervalize.
        #if not cumulative and not bin_width:
        if not bin_width:
            ifois = 0
            for sample in self.samples:
                # Don't add the Z' samples.
                if sample.is_zprime:
                    continue
                if ifois == 0:
                    mc_sum = sample.histogram.Clone()
                    ifois = 1
                else:
                    mc_sum.Add(sample.histogram, 1.)

            data_mc_diff = self.hdata.Clone()
            data_mc_diff.Divide(mc_sum)
            nbins = data_mc_diff.GetNbinsX()
            for ibin in range(1, nbins):
                f_bin = data_mc_diff.GetBinContent(ibin)
                data_mc_diff.SetBinContent(ibin, f_bin-1.)

        # Now draw the data on top of the stack.
        self.hdata.SetStats(0)
        data_draw_cmd = 'same p e'
        if self.use_poisson_intervals:
            self.hdata = poisson_intervalize(self.hdata, zero_ex=True,bin_width=bin_width)
            data_draw_cmd += ' z'
        if mymin is not None: self.hdata.SetMinimum(mymin)
        if mymax is not None: self.hdata.SetMaximum(mymax)
        self.hdata.SetMarkerStyle(20)
        self.hdata.SetMarkerSize(0.8)
        self.hdata.SetLineColor(ROOT.kBlack)
        self.hdata.Draw(data_draw_cmd)

        # Draw the Z' curve separately. It is overlaid, not stacked
        # with the rest of the MC expectation.
        zp = self.get_zprime_histogram()
        if self.should_draw_zprime(dilepton) and zp:
            # JMTBAD Extend to the rest of the Z' samples when there are any.
            zp.SetTitle('')
            zp.SetLineWidth(2)
            if xrange is not None:
                zp.GetXaxis().SetRangeUser(*xrange)
                zp.SetMinimum(mymin)
                zp.SetMaximum(mymax)
            zp.SetStats(0)
            zp.Draw('hist same')

        # Use log(x) whenever needed
        log_x = self.get_log_x(cutset, dilepton, quantity_to_compare)
        if log_x:
            self.ps.c.SetLogx(True)
            s.GetXaxis().SetNoExponent(True)

        self.ps.c.SetGridx(ROOT.kFALSE)
        self.ps.c.SetGridy(ROOT.kFALSE)

        # Adorn the plot with legend and labels.
        l = self.draw_legend(dilepton, cumulative, log_x)
        tcms = ROOT.TPaveLabel(0.10, 0.89, 0.50, 1.0, 'CMS','brNDC')
        tcms.SetTextAlign(12) # Left aligned
        tcms.SetTextSize(0.45)
        tcms.SetBorderSize(0)
        tcms.SetFillColor(0)
        tcms.SetFillStyle(0)
        tcms.SetTextFont(62) # Helvetica bold
        tcms.Draw()
        tpre = ROOT.TPaveLabel(0.18, 0.89, 0.50, 0.99, 'Preliminary','brNDC')
        tpre.SetTextAlign(12)
        tpre.SetTextSize(0.40)
        tpre.SetBorderSize(0)
        tpre.SetFillColor(0)
        tpre.SetFillStyle(0)
        tpre.SetTextFont(52) # Helvetica italics
        tpre.Draw()
        lumi = float(self.int_lumi)/1000.
        tlumi = ROOT.TPaveLabel(0.7, 0.89, 0.95, 1.0, ' %5.2f fb^{-1} (13 TeV)' %lumi , 'brNDC')
        tlumi.SetTextAlign(32) # Right aligned
        tlumi.SetTextSize(0.4)
        tlumi.SetBorderSize(0)
        tlumi.SetFillColor(0)
        tlumi.SetFillStyle(0)
        tlumi.SetTextFont(42) # Normal Helvetica
        tlumi.Draw()
                

        # Done; save it!
        plot_fn = dilepton
        if cumulative:
            plot_fn += '_cumulative'
        if bin_width:
            plot_fn += '_bin_width'
        self.ps.save(plot_fn)

        #if log_x:
        #    self.ps.c.SetLogx(0)

        #if not cumulative and not bin_width:
        if not bin_width:
            data_mc_diff.SetMinimum(-1.)
            data_mc_diff.SetMaximum(1.)
            data_mc_diff.SetMarkerStyle(20)
            data_mc_diff.SetMarkerSize(0.8)
            data_mc_diff.SetTitle(';%s;(data-bckg)/bckg' % xtitle)
            data_mc_diff.SetStats(0)
            data_mc_diff.Draw("p e")
            if log_x:
                data_mc_diff.GetXaxis().SetNoExponent(True)
            if xrange is not None:
                l1 = ROOT.TLine(xrange[0], 0., xrange[1],  0.)
            else:
                l1 = ROOT.TLine(data_mc_diff.GetXaxis().GetXmin(), 0., data_mc_diff.GetXaxis().GetXmax(), 0.)
            l1.Draw()
            tcms.Draw()
            tpre.Draw()
            tlumi.Draw()
            data_mc_diff.SetLineColor(ROOT.kBlack)
            self.ps.c.SetGrid(ROOT.kTRUE)
            plot_fn += '_diff'
            self.ps.save(plot_fn, log=False, pdf_log=False)
            
    def finalize_table(self, dir_base, cat):
        table_fn = os.path.join(dir_base, 'mass_counts.html')
        table_f = open(table_fn, 'wt')
        table_f.write('<html><body><pre>\n')
        table_f.write('\n'.join(self.advertise_lines(cat)) + '\n')
        last_cutset = None
        last_dilepton = None
        anchors = []
        for cutset, dilepton, mass_range in self.table_sections:
            anchor = cutset+dilepton+str(mass_range[0])
            if len(mass_range) > 1:
                anchor += str(mass_range[1])
            anchors.append(anchor)
                
            cutset = '%12s' % cutset
            dilepton = '%25s' % dilepton
            mass_range = '%15s' % repr(mass_range)

            text = ''
            if cutset != last_cutset:
                text += cutset
                last_cutset = cutset
            else:
                text += ' '*12
            if dilepton != last_dilepton:
                text += dilepton
                last_dilepton = dilepton
            else:
                text += ' '*20
            text += mass_range
            
            table_f.write('<a href="#%s">%s</a>\n'% (anchor, text))

        for row in self.table_rows:
            if 'ANCHORME' in row:
                row = '<h4 id="%s">%s</h4>' % (anchors.pop(0), row.replace('ANCHORME', ''))
            table_f.write(row)

        table_f.write('</pre></body></html>\n')
        table_f.close()
        self.table_sections = []
        self.table_rows = []

    def save_histos(self, cutset, dilepton, quantity_to_compare, cumulative):
        if cutset != 'Our2018':
            return
        if dilepton != 'MuonsPlusMuonsMinus' or dilepton!='MuonsOppSign':
            return
        if 'DimuonMass' not in quantity_to_compare:
            return

        zdy_ifois = 0
        prompt_ifois = 0
        for sample in self.samples:
            if sample.is_zprime:
                continue
            if 'dy' in sample.name or sample.name == 'zmumu':
                print 'dy: ',sample.name
                if zdy_ifois == 0:
                    zdy = sample.histogram.Clone('zdy')
                    zdy_ifois = 1
                else:
                    zdy.Add(sample.histogram, 1.)
            if sample.name in ('ttbar', 'ttbar_powheg', 'tW', 'tbarW', 'ztautau', 'WW', 'WZ', 'ZZ','Wjets'):
                print 'ttbar and others', sample.name
                if prompt_ifois == 0:
                    prompt = sample.histogram.Clone('prompt')
                    prompt_ifois = 1
                else:
                    prompt.Add(sample.histogram, 1.)
        data = self.hdata.Clone('data')
        data_tgraph = poisson_intervalize(self.hdata, zero_ex=True)
        data_tgraph.SetName("data_tgraph")

        file_name = 'dimuon_histos_differential.root'
        if cumulative:
            file_name = 'dimuon_histos_cumulative.root'

        histFile = ROOT.TFile.Open(file_name, 'recreate')
        if not histFile:
            raise RuntimeError, \
                  "Could not open '%s' as an output root file" % output
        data.Write()
        prompt.Write()
        zdy.Write()

        if not cumulative:
            nbins = data.GetNbinsX()
            data_tgraph_per_GeV = ROOT.TGraphAsymmErrors(data_tgraph)
            data_tgraph_per_GeV.SetName("data_tgraph_per_GeV")
            zdy_per_GeV         = zdy.Clone('zdy_per_GeV')
            prompt_per_GeV      = prompt.Clone('prompt_per_GeV')
            for i in xrange(1, nbins):
                c_data = data.GetBinContent(i)/data.GetBinWidth(i)
                e_data = data.GetBinError(i)/data.GetBinWidth(i)
                print i, 'nevents = ', data.GetBinContent(i), ' low edge = ', data.GetBinLowEdge(i), ' width = ', data.GetBinWidth(i), 'events/GeV = ', c_data, '+/-', e_data
                x        = data.GetBinLowEdge(i) + data.GetBinWidth(i)/2.
                err_low  = data_tgraph.GetErrorYlow(i-1)/data.GetBinWidth(i)
                err_high = data_tgraph.GetErrorYhigh(i-1)/data.GetBinWidth(i)
                print '  x = ', x, ' err_low = ', data_tgraph.GetErrorYlow(i-1), err_low, ' err_high = ', data_tgraph.GetErrorYhigh(i-1), err_high
                data_tgraph_per_GeV.SetPoint(i-1, x, c_data)
                data_tgraph_per_GeV.SetPointEYlow(i-1, err_low)
                data_tgraph_per_GeV.SetPointEYhigh(i-1, err_high)

                c_zdy = zdy.GetBinContent(i)/zdy.GetBinWidth(i)
                e_zdy = zdy.GetBinError(i)/zdy.GetBinWidth(i)
                zdy_per_GeV.SetBinContent(i, c_zdy)
                zdy_per_GeV.SetBinError(i, e_zdy)

                c_prompt = prompt.GetBinContent(i)/prompt.GetBinWidth(i)
                e_prompt = prompt.GetBinError(i)/prompt.GetBinWidth(i)
                prompt_per_GeV.SetBinContent(i, c_prompt)
                prompt_per_GeV.SetBinError(i, e_prompt)

            data_tgraph.Write()
            data_tgraph_per_GeV.Write()
            zdy_per_GeV.Write()
            prompt_per_GeV.Write()
        
    def go(self):
        for quantity_to_compare in self.quantities_to_compare:
            print quantity_to_compare
            if '_bb' in quantity_to_compare: cat = 'bb'
            elif '_be' in quantity_to_compare: cat = 'be'
            else: cat = ''
            
            #if quantity_to_compare != 'DileptonMass':
            #    cutsets = ['Our2018','Our2018MuPrescaled']
            #else:
            #    cutsets = self.cutsets
            cutsets = self.cutsets
            
            for cutset in cutsets:
                print cutset
                
                # If the cut set doesn't exist in the input file, silently skip it.
                #if not hasattr(self.data_f, self.get_dir_name(cutset, 'MuonsPlusMuonsMinus')):
                if not hasattr(self.data_f, self.get_dir_name(cutset, 'MuonsOppSign')):
                    continue

                # Directory structure example:
                # plot_dir_base = www_datamc/tag_dir/
                # plot_dir plot_dir/cutset/quantity_to_compare/.
                plot_dir = os.path.join(self.plot_dir_base,cutset,quantity_to_compare)
                self.ps.set_plot_dir(plot_dir)

                # Depending on the quantity to compare and cut set, skip certain dileptons.
                if cutset == 'EmuVeto': # Only care about e-mu dileptons here.
                    dileptons = [x for x in self.dileptons if 'Electron' in x]
                elif 'MuPrescaled' in cutset: # Don't care about e-mu dileptons here.
                    dileptons = [x for x in self.dileptons if 'Electron' not in x]
                else:
                    dileptons = [x for x in self.dileptons if 'MuonsAllSigns' not in x]
#                    dileptons = self.dileptons

                # Also depending on the quantity to be compared, skip certain
                # dileptons.
                if 'Dimuon' in quantity_to_compare: # Only defined for mumu.
                    dileptons = [x for x in dileptons if 'Electron' not in x]

                self.ps.save_dir('mass_counts.html')

                for dilepton in dileptons:
                    print dilepton
                    
                    for bin_width in (False, True):
                        for cumulative in (False, True):
                            # Cumulative histograms are meaningless for histograms normalized by bin width
                            if bin_width and cumulative: 
                                continue
                            # Prepare the histograms. The MC histograms are stored in
                            # their respective sample objects, and the data histogram is
                            # kept in self.hdata.
                            self.prepare_mc_histograms(cutset, dilepton, quantity_to_compare, cumulative, bin_width, cat)
                            self.prepare_data_histogram(cutset, dilepton, quantity_to_compare, cumulative, bin_width, cat)

                            #self.save_histos(cutset, dilepton, quantity_to_compare, cumulative)
                            
                            # Print the entries for the ASCII table for the current
                            # cutset+dilepton. Could extend this to support counts for
                            # ranges that aren't mass.
                            if ('DileptonMass' in quantity_to_compare or 'DimuonMassVertexConstrained' in quantity_to_compare):
                                if not cumulative and not bin_width and self.print_table:
                                    self.make_table(cutset, dilepton, quantity_to_compare)

                            if self.save_plots:
                                self.draw_data_on_mc(cutset, dilepton, quantity_to_compare, cumulative, bin_width)

                self.finalize_table(plot_dir,cat)


d = Drawer(options)
#for cat in ['','bb','be']:
#    print '\n'.join(d.advertise_lines(cat))
d.go()
