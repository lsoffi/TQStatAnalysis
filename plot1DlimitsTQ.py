import os
import sys
import ROOT
from array import array
import numpy as np
import json
from CMS_lumi import CMS_lumi
import plotting_interp as plot
ROOT.gROOT.SetBatch(ROOT.kTRUE)
plot.ModTDRStyle()

def run():

  model="TQ"
  m="26"
  filepath = 'TQ-jsons/'
  rootfile = ROOT.TFile(filepath+"plot_m"+m+"_2mu2e_2018.root","RECREATE")
  rootfile.cd()
#  wgt = 0.001/23.75  #0.001 b/c i injected this xsec in analysis.cpp 13.19 divided b/c theo presents limits in terms of BR
  wgt=1.

  # read in theoretical xsec
  xsecfile = open('crosssectionTQ.txt','r') 
  mstr = []
  masses = [26]
  xsecs = {} 
  xsec = []
  for line in xsecfile:
    line = line.rstrip('\n')
    line = line.split(' ')
    massstr = line[0]+'_2mu2e_2018'
#    print massstr
    mstr.append(massstr)
    xsecs[massstr] = float(line[1])

  xsec = array( 'd' )
  mass = array( 'd' )
  exp_raw = array( 'd' ) 
  obs_raw = array( 'd' ) 
  up1_raw = array( 'd' )
  do1_raw = array( 'd' )
  up2_raw = array( 'd' )
  do2_raw = array( 'd' )

  # pick up jsons with limits
  for m in masses:
 #   print m
    # make correct array of xsecs
    mass.append(m)
    xsec.append(xsecs[str(m)+'_2mu2e_2018'])   


    filename=filepath+'datacard_m'+massstr+'.json'
  #  print filename
    if os.path.isfile(filename):
      with open(filename) as jsonfile:
        data = json.load(jsonfile)
        for key in data: 
          exp_raw.append(data[key][u'exp0'])
          obs_raw.append(data[key][u'obs'])
          up1_raw.append(data[key][u'exp+1'])
          do1_raw.append(data[key][u'exp-1'])
          up2_raw.append(data[key][u'exp+2'])
          do2_raw.append(data[key][u'exp-2'])
          print data[key][u'exp0']
    else:  print 'File '+filename+' NOT found'

  exp = scaleBR(exp_raw,wgt) 
  obs = scaleBR(obs_raw,wgt)
  up1 = scaleBR(up1_raw,wgt)
  do1 = scaleBR(do1_raw,wgt)
  up2 = scaleBR(up2_raw,wgt)
  do2 = scaleBR(do2_raw,wgt)

  numpts = len(mass)          
  print("numpts:", numpts)
  print ("xsec: ",xsec)
  limitPlotExp = ROOT.TGraph(numpts,mass,exp)
  limitPlotObs = ROOT.TGraph(numpts,mass,obs)
  limitPlotXsc = ROOT.TGraph(numpts,mass,xsec)
  limitPlot1sig   = ROOT.TGraph(2*numpts)
  limitPlot2sig   = ROOT.TGraph(2*numpts)

  for i in range(0,numpts):
    limitPlotExp.SetPoint(i,mass[i],exp[i])
#    limitPlotExp.SetPoint(numpts+i,mass[numpts-i-1],do1[numpts-i-1])
    limitPlot1sig.SetPoint(i,mass[i],up1[i])
    limitPlot1sig.SetPoint(numpts+i,mass[numpts-i-1],do1[numpts-i-1])
    limitPlot2sig.SetPoint(i,mass[i],up2[i])
    limitPlot2sig.SetPoint(numpts+i,mass[numpts-i-1],do2[numpts-i-1])
  

  ROOT.gStyle.SetOptStat(0)
  c = ROOT.TCanvas('','')
#  c.SetLogx(1)
  c.SetLogy(1)
  c.SetGrid();
 
  limitPlotExp.SetTitle("")
  limitPlotExp.SetMarkerSize(3)
  limitPlotExp.GetXaxis().SetTitle(" TQ mass [GeV]")
  limitPlotExp.GetYaxis().SetTitle("#sigma BR(TQ#rightarrowXX#rightarrow 2#mu2e)")

  # styling
  limitPlotXsc.SetLineColor(4)
  limitPlotXsc.SetLineStyle(7)
  limitPlotXsc.SetLineWidth(2)

  limitPlotExp.SetLineStyle(7)
  limitPlotExp.SetLineWidth(2)
  limitPlotObs.SetLineWidth(2)

  limitPlot1sig.SetFillColor(5)
  limitPlot1sig.SetFillStyle(3013)

  limitPlot2sig.SetFillColor(8)
  limitPlot2sig.SetFillStyle(3013)

  limitPlotExp.SetMaximum(10000)
  limitPlotExp.SetMinimum(0.000000001)

  limitPlotExp.Draw("ACP")
  limitPlot2sig.Draw("F SAME")
  limitPlot1sig.Draw("F SAME")
  limitPlotExp.Draw("CP SAME")
#  limitPlotObs.Draw("CP SAME")
  limitPlotXsc.Draw("CP SAME")
  limitPlotExp.SetName("expected_curve")
  limitPlotExp.Write()
  
  CMS_lumi(c,4,0)
  c.RedrawAxis() 
  c.Print("~/www/TQ-WORK/limit_2mu2e_2018.pdf")
  c.Print("~/www/TQ-WORK/limit_2mu2e_2018.png")

 
def scaleBR(val,wgt):
   tmp = array('d')
   for i in val:
     scaledval= i * wgt
#     print scaledval
     tmp.append(i * wgt)
#   print tmp
   return tmp
  
if __name__=="__main__":
  run()
