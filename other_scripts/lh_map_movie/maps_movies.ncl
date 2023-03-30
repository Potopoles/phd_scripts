
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"


begin




yy = "2007"
mm = "02"

;#conv = "PARAM"
;#sim = "Atlantic_ppcc_PARAM_subhourly"
;#resol = "12km"
;#dd="01"
;#hh="00"
;#mmin = "00"

print(yy + mm + dd + hh + mmin)
    


dirmain = "/scratch/snx3000/lhentge/tmp_simulationdata_pp/data_atlantic_tests/" + sim +"/" + resol + "/2007/"
dirconst = "/scratch/snx3000/lhentge/tmp_simulationdata_pp/data_atlantic_tests/" + sim + "/" + resol + "/Z_CONSTVAR/"

filename_clcl = resol+"_evaluation_10min_CLCL_" + yy + mm + dd + hh + mmin + "00.nc"
filename_clcm = resol+"_evaluation_10min_CLCM_" + yy + mm + dd + hh + mmin + "00.nc"
filename_clch = resol+"_evaluation_10min_CLCH_" + yy + mm + dd + hh + mmin + "00.nc"
filename_tot_prec = resol+"_evaluation_10min_TOT_PREC_" + yy + mm + dd + hh + mmin + "00.nc"
filename_fr_land = "FR_LAND.nc"

file_clcl = addfile(dirmain + "CLCL/02/" + filename_clcl, "r")
file_clcm = addfile(dirmain + "CLCM/02/" + filename_clcm, "r")
file_clch = addfile(dirmain + "CLCH/02/" + filename_clch, "r")
file_tot_prec = addfile(dirmain + "TOT_PREC/02/" + filename_tot_prec, "r")
file_fr_land = addfile(dirconst + filename_fr_land, "r")


; dfile_fi = addfile(dfilename_fi + "p.nc", "r")
; cfile = addfile(cfilename , "r")
; cfile_fi = addfile(cfilename , "r")


clcl   = rm_single_dims(file_clcl->CLCL)
clcm   = rm_single_dims(file_clcm->CLCM)
clch   = rm_single_dims(file_clch->CLCH)
tot_prec   = rm_single_dims(file_tot_prec->TOT_PREC)
fr_land   = rm_single_dims(file_fr_land->FR_LAND)



tot_prec@long_name = ""
tot_prec@units     = ""
;#fi@long_name = ""
;#fi@units     = ""
clcl@long_name = ""
clcl@units     = ""
clcm@long_name = ""
clcm@units     = ""
clch@long_name = ""
clch@units     = ""


;#Filter out small rain
tot_prec@_FillValue=0
;# fi@_FillValue=-9999
clcl@_FillValue=-9999
clcm@_FillValue=-9999
clch@_FillValue=-9999

; Create Cloud Mask
;=============================================================
;Init
mask_clc = clcl

; Tuning Parametes for clouds
m_srf = 0.15
m_clcl = 1.0    ;0.2
m_clcm = 0.25    ;0.3
m_clch = 0.1    ;1.0

;Increase "temperature over iland points"
srf=where(fr_land.lt.0.5,0,m_srf)

;x_clcl = clcl * (m_clcl - srf) + srf
;x_clcm = x_clcl + clcm * (m_clcm - x_clcl)
;x_clch = x_clcm + clch * (m_clch - x_clcm)
;mask_clc = 1000.0 + clcl

x_clch = clch + (m_clch - srf) + srf
x_clcm = x_clch + clcm * (m_clcm - x_clch)
x_clcl = x_clcm + clcl * (m_clcl - x_clcm)
mask_clc = 1000.0 + x_clcl



;==============================================================

cmap = (/"(/1, 1, 1, 1/)",\
         "(/0,0,0,1/)",\
         "white",\
         "(/0.1960784, 0.6509804, 0.5882353, 1/)", \
         "(/0.01960784, 0.3137255, 0.5490196, 1/)", \
         "(/0.03921569,0.1215686,0.5882353, 1/)", \
         "(/0.4156863, 0.17254, 0.3529412, 1/)", \
         "firebrick", \
         "darkorange3",\
         "darkorange1", \
         "goldenrod2", \
         "(/0.05, 0.05, 0.05, 1/)",\
         "(/0.1, 0.1, 0.1, 1/)", \
         "(/0.15,0.15,0.15,1/)", \
         "(/0.2,0.2,0.2,1/)", \
         "(/0.25, 0.25, 0.25, 1/)", \
         "(/0.3,0.3,0.3,1/)", \
         "(/0.35,0.35,0.35,1/)", \
         "(/0.4, 0.4, 0.4, 1/)", \
         "(/0.45,0.45,0.45,1/)", \
         "(/0.5,0.5,0.5,1/)", \
         "(/0.55, 0.55, 0.55, 1/)",\
         "(/0.6,0.6,0.6,1/)",\
         "(/0.65,0.65,0.65,1/)", \
         "(/0.6, 0.6, 0.6, 1/)", \
         "(/0.65,0.65,0.65,1/)", \
         "(/0.7,0.7,0.7,1/)", \
         "(/0.75, 0.75, 0.75, 1/)", \
         "(/0.8,0.8,0.8,1/)", \
         "(/0.85,0.85,0.85,1/)", \
         "(/0.9, 0.9, 0.9, 1/)", \
         "(/0.95, 0.95, 0.95, 1/)", \
         "(/1, 1, 1, 1/)", \
         "(/0, 0, 0, -1/)"/)

dirplot = "/scratch/snx3000/lhentge/tmp_movies/" + conv + "_" + resol + "/"
;#dirplot = "/users/lhentge/"

filename = "test" + yy + mm + dd + hh + mmin + "00"

wks_type = "png"
wks_type@wkWidth = 4000
wks_type@wkHeight = 4000
wks = gsn_open_wks(wks_type, dirplot+ filename )
gsn_define_colormap(wks,cmap)

setvalues wks
  "wkBackgroundColor" : "black"
  "wkForegroundColor" : "white"
end setvalues
;==============================================================

res                       = True
res@gsnDraw               = False
res@gsnFrame              = False
res@tiYAxisString         = ""
res@tiXAxisString         = ""
res@gsnMaximize           = True
res@gsnPaperOrientation   = "portrait"
mpres                     = res
sres                      = res

res@cnFillOn              = True
res@cnFillDrawOrder       = "Predraw"
res@cnFillMode            = "CellFill"
res@cnLinesOn             = False
res@cnLineLabelsOn        = False
res@cnInfoLabelOn         = False

res@lbLabelBarOn           = False
res@cnNoDataLabelOn        = False

res@cnLevelSelectionMode = "ExplicitLevels" ; set explicit contour levels

clcres                    = res
res@cnFillOpacityF        = 0.7

;Define the underlying map
;-------------------------
mpres@mpProjection           = "Mercator"
mpres@mpFillOn               = False
mpres@mpOutlineSpecifiers    = "Ocean"
mpres@mpGeophysicalLineColor = "white"
mpres@mpDataBaseVersion      = "HighRes"
mpres@mpDataBaseVersion      = "Ncarg4_1"
mpres@mpDataSetName          = "Earth..4"
mpres@pmTickMarkDisplayMode  = "Never"
mpres@mpGeophysicalLineThicknessF = 8
;mpres@mpNationalLineThicknessF= 2
mpres@mpLabelsOn             = False
mpres@mpOutlineOn            = True
mpres@mpOutlineDrawOrder     = "PostDraw"
;# mpres@mpCenterLonF           = tot_prec@lon ;#lontot_prec@pollon + 180.
;# mpres@mpCenterLatF           = tot_prec@lat ;#90. - tot_prec@pollat

;# mpres@mpLimitMode            = "Corners"
mpres@mpLimitMode            = "LatLon"



mpres@mpMinLatF = -6.77 ;#-7.77 ;# minmaxlatlon@MinLat
mpres@mpMaxLatF = 22.07 ;# 23.07 ;# minmaxlatlon@MaxLat
mpres@mpMinLonF = -64.625   ;#-65.625 ;# minmaxlatlon@MinLon
mpres@mpMaxLonF = -20.425   ;#-19.42 ;# minmaxlatlon@MaxLon



;Add pressure contours
;---------------------
; XXXXXXXXX





;=============================================================
plot := gsn_csm_map(wks,mpres)

;plot rain
;res@cnLevels = (/ 0.2, 0.5, 1, 2, 5, 10, 20, 50 /) ; set levels
res@cnLevels := (/ 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5 /) ; set levels
res@cnFillColors   := (/2,3,4,5,6,7,8,9,10,11/)
plot_rain := gsn_csm_contour(wks,tot_prec(:,:),res)

; Plot clouds
clcres@cnLevels       := (/ 1000.05, 1000.1,  1000.15,1000.2,  1000.25,1000.3,  1000.35,1000.4, 1000.45,1000.5, 1000.55, \
                           1000.6,  1000.65, 1000.7, 1000.75, 1000.8, 1000.85, 1000.9, 1000.95,1001.0/) ; set levels
clcres@cnFillColors   := (/11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31/)
plot_clc = gsn_csm_contour(wks,mask_clc,clcres)

;Plot geopot
;# plot_fi = gsn_csm_contour(wks,fi(0,:,:),sres)




;#txres               = True                     ; text mods desired
;#txres@txFontHeightF = 1                     ; font smaller. default big
;#txres@txFontColor = "blue"
;#dum = gsn_add_text(wks,plot_clc,"Text in Plot Coordinates",1,1,txres)



;overlay(plot,plot_rain)
overlay(plot,plot_clc)
overlay(plot,plot_rain)
;# overlay(plot,plot_fi)


txres3               = True                     ; text mods desired
txres3@txFontHeightF =0.023                    ; font smaller. default big
txres3@txBackgroundFillColor = "black"
txres3@txFontColor = "white"
txres3@txFont        = 22
;#gsn_text_ndc(wks, "dx = 2.2 km"  ,0.15, 0.86  ,txres3)
gsn_text_ndc(wks, "dx = 12 km"  ,0.15, 0.86  ,txres3)



txres4               = True                     ; text mods desired
txres4@txFontHeightF =0.023                    ; font smaller. default big
txres4@txBackgroundFillColor = "black"
txres4@txFontColor = "white"
txres4@txFont        = 22
str_time = tostring(dd) + " FEB 2007 " + " " + " " + tostring(hh)+ ":" + tostring(mmin)
gsn_text_ndc(wks, str_time  ,0.82, 0.86  ,txres4)



draw(plot)
frame(wks)









end
