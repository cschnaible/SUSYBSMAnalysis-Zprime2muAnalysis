import ROOT as R
import numpy as np
import sys,os,array

def draw_overflow(hist,underflow):
    # Function to paint the histogram hist with an extra bin for overflows
    nx = hist.GetNbinsX()+1+(1 if underflow else 0)
    xbins = array.array('d',[])
    if underflow:
        for ibin in range(nx+1):
            if ibin==0: xbins.append(hist.GetBinLowEdge(1)-hist.GetBinWidth(1))
            elif ibin==nx+1: xbins.append(xbins[nx-1]+hist.GetBinWidth(nx))
            else: xbins.append(hist.GetBinLowEdge(ibin))
    else:
        for ibin in range(nx+1):
            if ibin==nx+1: xbins.append(xbins[nx-1]+hist.GetBinWidth(nx))
            else: xbins.append(hist.GetBinLowEdge(ibin+1))
    # Book a temporary histogram having extra bins for overflows
    newname = hist.GetName()+'_'+('under' if underflow else '')+'overflow'
    htmp = R.TH1F(newname, hist.GetTitle(), nx, xbins)
    htmp.Sumw2()
    # Fill the new histogram including the overflows
    for ibin in range(0,nx+1):
        if underflow:
            htmp.SetBinContent(htmp.FindBin(htmp.GetBinCenter(ibin+1)),hist.GetBinContent(ibin))
            htmp.SetBinError(htmp.FindBin(htmp.GetBinCenter(ibin+1)),hist.GetBinError(ibin))
        else:
            if ibin==0: continue
            htmp.SetBinContent(htmp.FindBin(htmp.GetBinCenter(ibin)),hist.GetBinContent(ibin))
            htmp.SetBinError(htmp.FindBin(htmp.GetBinCenter(ibin)),hist.GetBinError(ibin))
    # Do the underflows but don't paint
    if not underflow:
        htmp.SetBinContent(htmp.FindBin(htmp.GetBinCenter(1)-1),hist.GetBinContent(0))
        htmp.SetBinError(htmp.FindBin(htmp.GetBinCenter(1)-1),hist.GetBinError(0))
    # Restore the number of entries
    htmp.SetEntries(hist.GetEffectiveEntries())
    return htmp

def divide_bin_width(h):
    '''Need to do this by hand since I want to allow for
    variable bin widths'''
    hnew = h.Clone(h.GetName()+'_bw')
    nbins = h.GetNbinsX()
    for i in range(1,nbins+1):
        c = h.GetBinContent(i)
        e = h.GetBinError(i)
        w = h.GetXaxis().GetBinUpEdge(i) - h.GetXaxis().GetBinLowEdge(i)
        hnew.SetBinContent(i,c/w)
        hnew.SetBinError(i,e/w)
        #print c,e,w
    return hnew

def poisson_interval(nobs, alpha=(1-0.6827)/2, beta=(1-0.6827)/2):
    lower = 0
    if nobs > 0:
        lower = 0.5 * ROOT.Math.chisquared_quantile_c(1-alpha, 2*nobs)
    elif nobs == 0:
        beta *= 2
    upper = 0.5 * ROOT.Math.chisquared_quantile_c(beta, 2*(nobs+1))
    return lower, upper

def poisson_intervalize(h, zero_x=False, include_zero_bins=False):
    h2 = ROOT.TGraphAsymmErrors(h)
    for i in xrange(1, h.GetNbinsX()+1):
        c = h.GetBinContent(i)
        if c == 0 and not include_zero_bins:
            continue
        l,u = poisson_interval(c)
        # i-1 in the following because ROOT TGraphs count from 0 but
        # TH1s count from 1
        if zero_x:
            h2.SetPointEXlow(i-1, 0)
            h2.SetPointEXhigh(i-1, 0)
        h2.SetPointEYlow(i-1, c-l)
        h2.SetPointEYhigh(i-1, u-c)
    return h2

def clopper_pearson(n_on, n_tot, alpha=1-0.6827, equal_tailed=True):
    if equal_tailed:
        alpha_min = alpha/2
    else:
        alpha_min = alpha

    lower = 0
    upper = 1

    if n_on > 0:
        lower = ROOT.Math.beta_quantile(alpha_min, n_on, n_tot - n_on + 1)
    if n_tot - n_on > 0:
        upper = ROOT.Math.beta_quantile_c(alpha_min, n_on + 1, n_tot - n_on)

    if n_on == 0 and n_tot == 0:
        return 0, lower, upper
    else:
        return float(n_on)/n_tot, lower, upper

def clopper_pearson_poisson_means(x, y, alpha=1-0.6827):
    r, rl, rh = clopper_pearson(x, x+y, alpha)
    return r/(1 - r), rl/(1 - rl), rh/(1 - rh)

def binomial_divide(h1, h2, confint=clopper_pearson, force_lt_1=True):
    nbins = h1.GetNbinsX()
    xax = h1.GetXaxis()
    if h2.GetNbinsX() != nbins: # or xax2.GetBinLowEdge(1) != xax.GetBinLowEdge(1) or xax2.GetBinLowEdge(nbins) != xax.GetBinLowEdge(nbins):
        raise ValueError, 'incompatible histograms to divide'
    x = []
    y = []
    exl = []
    exh = []
    eyl = []
    eyh = []
    xax = h1.GetXaxis()
    for ibin in xrange(1, nbins+1):
        s,t = h1.GetBinContent(ibin), h2.GetBinContent(ibin)
        if t == 0:
            assert(s == 0)
            continue

        p_hat = float(s)/t
        if s > t and force_lt_1:
            print 'warning: bin %i has p_hat > 1, in interval forcing p_hat = 1' % ibin
            s = t
        rat, a,b = confint(s,t)
        #print ibin, s, t, a, b

        _x  = xax.GetBinCenter(ibin)
        #print "x", _x
        _xw = xax.GetBinWidth(ibin)/2
        #print "xw", _xw
        
        x.append(_x)
        exl.append(_xw)
        exh.append(_xw)

        y.append(p_hat)
        eyl.append(p_hat - a)
        eyh.append(b - p_hat)
    eff = ROOT.TGraphAsymmErrors(len(x), *[array('d', obj) for obj in (x,y,exl,exh,eyl,eyh)])
    return eff, y, eyl, eyh

def core_gaussian(hist, factor, i=[0]):
    core_mean  = hist.GetMean()
    core_width = factor*hist.GetRMS()
    f = ROOT.TF1('core%i' % i[0], 'gaus', core_mean - core_width, core_mean + core_width)
    i[0] += 1
    return f

def cumulative_histogram(h, type='ge'):
    """Construct the cumulative histogram in which the value of each
    bin is the tail integral of the given histogram.
    """
    
    nb = h.GetNbinsX()
    hc = ROOT.TH1F(h.GetName() + '_cumulative_' + type, '', nb, h.GetXaxis().GetXmin(), h.GetXaxis().GetXmax())
    hc.Sumw2()
    if type == 'ge':
        first, last, step = nb+1, 0, -1
    elif type == 'le':
        first, last, step = 0, nb+1, 1
    else:
        raise ValueError('type %s not recognized' % type)
    for i in xrange(first, last, step):
        prev = 0 if i == first else hc.GetBinContent(i-step)
        c = h.GetBinContent(i) + prev
        hc.SetBinContent(i, c)
        if c > 0:
            hc.SetBinError(i, c**0.5)
        else:
            hc.SetBinError(i, 0.)
    return hc

def fit_gaussian(hist, factor=None, draw=False, cache=[]):
    """Fit a Gaussian to the histogram, and return a dict with fitted
    parameters and errors. If factor is supplied, fit only to range in
    hist.mean +/- factor * hist.rms.
    """

    if draw:
        opt = 'qr'
    else:
        opt = 'qr0'

    if factor is not None:
        fcn = core_gaussian(hist, factor)
        cache.append(fcn)
        hist.Fit(fcn, opt)
    else:
        hist.Fit('gaus', opt)
        fcn = hist.GetFunction('gaus')
        
    return {
        'constant': (fcn.GetParameter(0), fcn.GetParError(0)),
        'mu':       (fcn.GetParameter(1), fcn.GetParError(1)),
        'sigma':    (fcn.GetParameter(2), fcn.GetParError(2))
        }
    
def get_bin_content_error(hist, value):
    """For the given histogram, find the bin corresponding to the
    value and return its contents and associated
    error. Multi-dimensional histograms are supported; value may be a
    tuple in those cases.
    """

    if type(value) != type(()):
        value = (value,)
    bin = hist.FindBin(*value)
    return (hist.GetBinContent(bin), hist.GetBinError(bin))

def get_integral(hist, xlo, xhi=None, integral_only=False, include_last_bin=True, nm1=False):
    """For the given histogram, return the integral of the bins
    corresponding to the values xlo to xhi along with its error.

    Edited to return 0 if integral is negative (for N-1 calculation 
    to prevent negative efficeincy when events have negative weights)
    """
    
    binlo = hist.FindBin(xlo)
    if xhi is None:
        binhi = hist.GetNbinsX()+1
    else:
        binhi = hist.FindBin(xhi)
        if not include_last_bin:
            binhi -= 1

    integral = hist.Integral(binlo, binhi)
    if integral_only:
        if nm1 and integral < 0:
            return 0
        else:
            return integral

    wsq = 0
    for i in xrange(binlo, binhi+1):
        wsq += hist.GetBinError(i)**2
    if nm1 and integral < 0:
        return 0,0
    else:
        return integral, wsq**0.5

def get_hist_stats(hist, factor=None, draw=False):
    """For the given histogram, return a five-tuple of the number of
    entries, the underflow and overflow counts, the fitted sigma
    (using the function specified by fcnname, which must be an
    already-made ROOT.TF1 whose parameter(2) is the value used), and the
    RMS.
    """
    
    results = fit_gaussian(hist, factor, draw)
    results.update({
        'entries': hist.GetEntries(),
        'under':   hist.GetBinContent(0),
        'over':    hist.GetBinContent(hist.GetNbinsX()+1),
        'mean':    (hist.GetMean(), hist.GetMeanError()),
        'rms':     (hist.GetRMS(), hist.GetRMSError())
        })
    return results

def make_rms_hist(prof, name='', bins=None, cache={}):
    """Takes an input TProfile and produces a histogram whose bin contents are
    the RMS of the bins of the profile. Caches the histogram so that it doesn't
    get deleted by python before it gets finalized onto a TCanvas.

    If bins is a list of bin lower edges + last bin high edge,
    rebinning is done before making the RMS histogram. Due to a bug in
    ROOT's TProfile in versions less than 5.22 (?), rebinning is done
    manually here.
    """
    
    nbins = prof.GetNbinsX()
    if name == '':
        name = 'RMS' + prof.GetName()
    title = 'RMS ' + prof.GetTitle()
    old_axis = prof.GetXaxis()

    # Play nice with same-name histograms that were OK because they
    # were originally in different directories.
    while cache.has_key(name):
        name += '1'

    # Format of contents list: [(new_bin, (new_bin_content, new_bin_error)), ...]
    contents = []
    
    if bins:
        if type(bins) == type([]):
            bins = array('f', bins)
        new_hist = ROOT.TH1F(name, title, len(bins)-1, bins)
        new_axis = new_hist.GetXaxis()
        new_bins = {}
        for old_bin in xrange(1, nbins+1):
            new_bin = new_axis.FindBin(old_axis.GetBinLowEdge(old_bin))
            if not new_bins.has_key(new_bin):
                new_bins[new_bin] = [0., 0.]
            N = prof.GetBinEntries(old_bin)
            new_bins[new_bin][0] += N*prof.GetBinContent(old_bin)
            new_bins[new_bin][1] += N
        for val in new_bins.values():
            if val[1] > 0:
                val[0] /= val[1]
        contents = new_bins.items()
    else:
        new_hist = ROOT.TH1F(name, title, nbins, old_axis.GetXmin(), old_axis.GetXmax())
        for old_bin in xrange(1, nbins+1):
            f_bin = float(prof.GetBinContent(old_bin))
            ent_bin = float(prof.GetBinEntries(old_bin))
            contents.append((old_bin, (f_bin, ent_bin)))

    for new_bin, (f_bin, ent_bin) in contents:
        if f_bin > 0:
            f_bin = f_bin**0.5
        else:
            f_bin = 0
            
        if ent_bin > 0:
            err_bin = f_bin/(2.*ent_bin)**0.5
        else:
            err_bin = 0

        new_hist.SetBinContent(new_bin, f_bin)
        new_hist.SetBinError(new_bin, err_bin)
        
    cache[name] = new_hist
    return new_hist

def move_below_into_bin(h,a):
    """Given the TH1 h, add the contents of the bins below the one
    corresponding to a into that bin, and zero the bins below."""
    assert(h.Class().GetName().startswith('TH1')) # i bet there's a better way to do this...
    b = h.FindBin(a)
    bc = h.GetBinContent(b)
    bcv = h.GetBinError(b)**2
    for nb in xrange(0, b):
        bc += h.GetBinContent(nb)
        bcv += h.GetBinError(nb)**2
        h.SetBinContent(nb, 0)
        h.SetBinError(nb, 0)
    h.SetBinContent(b, bc)
    h.SetBinError(b, bcv**0.5)

def move_above_into_bin(h,a):
    """Given the TH1 h, add the contents of the bins above the one
    corresponding to a into that bin, and zero the bins above."""
    assert(h.Class().GetName().startswith('TH1')) # i bet there's a better way to do this...
    b = h.FindBin(a)
    bc = h.GetBinContent(b)
    bcv = h.GetBinError(b)**2
    for nb in xrange(b+1, h.GetNbinsX()+2):
        bc += h.GetBinContent(nb)
        bcv += h.GetBinError(nb)**2
        h.SetBinContent(nb, 0)
        h.SetBinError(nb, 0)
    h.SetBinContent(b, bc)
    h.SetBinError(b, bcv**0.5)

def move_overflow_into_last_bin(h):
    """Given the TH1 h, Add the contents of the overflow bin into the
    last bin, and zero the overflow bin."""
    assert(h.Class().GetName().startswith('TH1')) # i bet there's a better way to do this...
    nb = h.GetNbinsX()
    h.SetBinContent(nb, h.GetBinContent(nb) + h.GetBinContent(nb+1))
    h.SetBinError(nb, (h.GetBinError(nb)**2 + h.GetBinError(nb+1)**2)**0.5)
    h.SetBinContent(nb+1, 0)
    h.SetBinError(nb+1, 0)

def real_hist_max(h, return_bin=False, user_range=None, use_error_bars=True):
    """Find the real maximum value of the histogram, taking into
    account the error bars and/or the specified range."""

    m_ibin = None
    m = 0

    if user_range is None:
        b1, b2 = 1, h.GetNbinsX() + 1
    else:
        b1, b2 = h.FindBin(user_range[0]), h.FindBin(user_range[1])#####
        #b1, b2 = h.FindBin(user_range[0]), h.FindBin(user_range[1])+1
    for ibin in xrange(b1, b2):
        if use_error_bars:
            v = h.GetBinContent(ibin) + h.GetBinError(ibin)
        else:
            v = h.GetBinContent(ibin)
        if v > m:
            m = v
            m_ibin = ibin
    if return_bin:
        return m_ibin, m
    else:
        return m

def real_hist_min(h, return_bin=False, user_range=None):
    """Find the real minimum value of the histogram, ignoring empty
    bins, and taking into account the specified range."""

    m_ibin = None
    m = 99e99

    if user_range is None:
        b1, b2 = 1, h.GetNbinsX() + 1
    else:
        b1, b2 = h.FindBin(user_range[0]), h.FindBin(user_range[1])+1
    
    for ibin in xrange(b1, b2):
        v = h.GetBinContent(ibin)
        if v > 0 and v < m:
            m = v
            m_ibin = ibin
    if return_bin:
        return m_ibin, m
    else:
        return m
