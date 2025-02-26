<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="9.7.0">
<drawing>
<settings>
<setting alwaysvectorfont="no"/>
<setting verticaltext="up"/>
</settings>
<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="no" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
<layer number="1" name="Top" color="4" fill="1" visible="no" active="no"/>
<layer number="2" name="Route2" color="16" fill="1" visible="no" active="no"/>
<layer number="3" name="Route3" color="17" fill="1" visible="no" active="no"/>
<layer number="4" name="Route4" color="18" fill="1" visible="no" active="no"/>
<layer number="5" name="Route5" color="19" fill="1" visible="no" active="no"/>
<layer number="6" name="Route6" color="25" fill="1" visible="no" active="no"/>
<layer number="7" name="Route7" color="26" fill="1" visible="no" active="no"/>
<layer number="8" name="Route8" color="27" fill="1" visible="no" active="no"/>
<layer number="9" name="Route9" color="28" fill="1" visible="no" active="no"/>
<layer number="10" name="Route10" color="29" fill="1" visible="no" active="no"/>
<layer number="11" name="Route11" color="30" fill="1" visible="no" active="no"/>
<layer number="12" name="Route12" color="20" fill="1" visible="no" active="no"/>
<layer number="13" name="Route13" color="21" fill="1" visible="no" active="no"/>
<layer number="14" name="Route14" color="22" fill="1" visible="no" active="no"/>
<layer number="15" name="Route15" color="23" fill="1" visible="no" active="no"/>
<layer number="16" name="Bottom" color="1" fill="1" visible="no" active="no"/>
<layer number="17" name="Pads" color="2" fill="1" visible="no" active="no"/>
<layer number="18" name="Vias" color="2" fill="1" visible="no" active="no"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="no" active="no"/>
<layer number="20" name="Dimension" color="24" fill="1" visible="no" active="no"/>
<layer number="21" name="tPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="25" name="tNames" color="7" fill="1" visible="no" active="no"/>
<layer number="26" name="bNames" color="7" fill="1" visible="no" active="no"/>
<layer number="27" name="tValues" color="7" fill="1" visible="no" active="no"/>
<layer number="28" name="bValues" color="7" fill="1" visible="no" active="no"/>
<layer number="29" name="tStop" color="7" fill="3" visible="no" active="no"/>
<layer number="30" name="bStop" color="7" fill="6" visible="no" active="no"/>
<layer number="31" name="tCream" color="7" fill="4" visible="no" active="no"/>
<layer number="32" name="bCream" color="7" fill="5" visible="no" active="no"/>
<layer number="33" name="tFinish" color="6" fill="3" visible="no" active="no"/>
<layer number="34" name="bFinish" color="6" fill="6" visible="no" active="no"/>
<layer number="35" name="tGlue" color="7" fill="4" visible="no" active="no"/>
<layer number="36" name="bGlue" color="7" fill="5" visible="no" active="no"/>
<layer number="37" name="tTest" color="7" fill="1" visible="no" active="no"/>
<layer number="38" name="bTest" color="7" fill="1" visible="no" active="no"/>
<layer number="39" name="tKeepout" color="4" fill="11" visible="no" active="no"/>
<layer number="40" name="bKeepout" color="1" fill="11" visible="no" active="no"/>
<layer number="41" name="tRestrict" color="4" fill="10" visible="no" active="no"/>
<layer number="42" name="bRestrict" color="1" fill="10" visible="no" active="no"/>
<layer number="43" name="vRestrict" color="2" fill="10" visible="no" active="no"/>
<layer number="44" name="Drills" color="7" fill="1" visible="no" active="no"/>
<layer number="45" name="Holes" color="7" fill="1" visible="no" active="no"/>
<layer number="46" name="Milling" color="3" fill="1" visible="no" active="no"/>
<layer number="47" name="Measures" color="7" fill="1" visible="no" active="no"/>
<layer number="48" name="Document" color="7" fill="1" visible="no" active="no"/>
<layer number="49" name="Reference" color="7" fill="1" visible="no" active="no"/>
<layer number="51" name="tDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="88" name="SimResults" color="9" fill="1" visible="yes" active="yes"/>
<layer number="89" name="SimProbes" color="9" fill="1" visible="yes" active="yes"/>
<layer number="90" name="Modules" color="5" fill="1" visible="yes" active="yes"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="no" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
</layers>
<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">
<libraries>
<library name="RpiPico">
<packages>
<package name="PICO-PKG">
<wire x1="10.5" y1="-25.5" x2="10.5" y2="-24.63" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-23.63" x2="10.5" y2="-22.09" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-21.09" x2="10.5" y2="-19.55" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-18.55" x2="10.5" y2="-17.01" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-16.01" x2="10.5" y2="-14.47" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-13.47" x2="10.5" y2="-11.93" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-10.93" x2="10.5" y2="-9.39" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-8.39" x2="10.5" y2="-6.85" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-5.85" x2="10.5" y2="-4.31" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-3.31" x2="10.5" y2="-1.77" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-0.77" x2="10.5" y2="0.77" width="0.1524" layer="21"/>
<wire x1="10.5" y1="1.77" x2="10.5" y2="3.31" width="0.1524" layer="21"/>
<wire x1="10.5" y1="4.31" x2="10.5" y2="5.85" width="0.1524" layer="21"/>
<wire x1="10.5" y1="6.85" x2="10.5" y2="8.39" width="0.1524" layer="21"/>
<wire x1="10.5" y1="9.39" x2="10.5" y2="10.93" width="0.1524" layer="21"/>
<wire x1="10.5" y1="11.93" x2="10.5" y2="13.47" width="0.1524" layer="21"/>
<wire x1="10.5" y1="14.47" x2="10.5" y2="16.01" width="0.1524" layer="21"/>
<wire x1="10.5" y1="17.01" x2="10.5" y2="18.55" width="0.1524" layer="21"/>
<wire x1="10.5" y1="19.55" x2="10.5" y2="21.09" width="0.1524" layer="21"/>
<wire x1="10.5" y1="22.09" x2="10.5" y2="23.63" width="0.1524" layer="21"/>
<wire x1="10.5" y1="24.63" x2="10.5" y2="25.5" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="25.5" x2="-10.5" y2="24.63" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="23.63" x2="-10.5" y2="22.09" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="21.09" x2="-10.5" y2="19.55" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="18.55" x2="-10.5" y2="17.01" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="16.01" x2="-10.5" y2="14.47" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="13.47" x2="-10.5" y2="11.93" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="10.93" x2="-10.5" y2="9.39" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="8.39" x2="-10.5" y2="6.85" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="5.85" x2="-10.5" y2="4.31" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="3.31" x2="-10.5" y2="1.77" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="0.77" x2="-10.5" y2="-0.77" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-1.77" x2="-10.5" y2="-3.31" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-4.31" x2="-10.5" y2="-5.85" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-6.85" x2="-10.5" y2="-8.39" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-9.39" x2="-10.5" y2="-10.93" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-11.93" x2="-10.5" y2="-13.47" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-14.47" x2="-10.5" y2="-16.01" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-17.01" x2="-10.5" y2="-18.55" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-19.55" x2="-10.5" y2="-21.09" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-22.09" x2="-10.5" y2="-23.63" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-24.63" x2="-10.5" y2="-25.5" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-25.5" x2="3.04" y2="-25.5" width="0.1524" layer="21"/>
<wire x1="2.04" y1="-25.5" x2="0.5" y2="-25.5" width="0.1524" layer="21"/>
<wire x1="-0.5" y1="-25.5" x2="-2.04" y2="-25.5" width="0.1524" layer="21"/>
<wire x1="-3.04" y1="-25.5" x2="-10.5" y2="-25.5" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="25.5" x2="10.5" y2="25.5" width="0.1524" layer="21"/>
<pad name="1" x="-8.89" y="24.13" drill="1"/>
<pad name="2" x="-8.89" y="21.59" drill="1"/>
<pad name="7" x="-8.89" y="8.89" drill="1"/>
<pad name="8" x="-8.89" y="6.35" drill="1"/>
<pad name="3" x="-8.89" y="19.05" drill="1"/>
<pad name="4" x="-8.89" y="16.51" drill="1"/>
<pad name="6" x="-8.89" y="11.43" drill="1"/>
<pad name="5" x="-8.89" y="13.97" drill="1"/>
<pad name="9" x="-8.89" y="3.81" drill="1"/>
<pad name="10" x="-8.89" y="1.27" drill="1"/>
<pad name="11" x="-8.89" y="-1.27" drill="1"/>
<pad name="12" x="-8.89" y="-3.81" drill="1"/>
<pad name="13" x="-8.89" y="-6.35" drill="1"/>
<pad name="14" x="-8.89" y="-8.89" drill="1"/>
<pad name="15" x="-8.89" y="-11.43" drill="1"/>
<pad name="16" x="-8.89" y="-13.97" drill="1"/>
<pad name="17" x="-8.89" y="-16.51" drill="1"/>
<pad name="18" x="-8.89" y="-19.05" drill="1"/>
<pad name="19" x="-8.89" y="-21.59" drill="1"/>
<pad name="20" x="-8.89" y="-24.13" drill="1"/>
<pad name="21" x="8.89" y="-24.13" drill="1"/>
<pad name="22" x="8.89" y="-21.59" drill="1"/>
<pad name="23" x="8.89" y="-19.05" drill="1"/>
<pad name="24" x="8.89" y="-16.51" drill="1"/>
<pad name="25" x="8.89" y="-13.97" drill="1"/>
<pad name="26" x="8.89" y="-11.43" drill="1"/>
<pad name="27" x="8.89" y="-8.89" drill="1"/>
<pad name="28" x="8.89" y="-6.35" drill="1"/>
<pad name="29" x="8.89" y="-3.81" drill="1"/>
<pad name="30" x="8.89" y="-1.27" drill="1"/>
<pad name="31" x="8.89" y="1.27" drill="1"/>
<pad name="32" x="8.89" y="3.81" drill="1"/>
<pad name="33" x="8.89" y="6.35" drill="1"/>
<pad name="34" x="8.89" y="8.89" drill="1"/>
<pad name="35" x="8.89" y="11.43" drill="1"/>
<pad name="36" x="8.89" y="13.97" drill="1"/>
<pad name="37" x="8.89" y="16.51" drill="1"/>
<pad name="38" x="8.89" y="19.05" drill="1"/>
<pad name="39" x="8.89" y="21.59" drill="1"/>
<pad name="40" x="8.89" y="24.13" drill="1"/>
<text x="-10.414" y="-28.067" size="1.778" layer="25">&gt;NAME</text>
<text x="1.016" y="-20.955" size="1.778" layer="27" rot="R90">&gt;VALUE</text>
<smd name="P$1" x="-10" y="24.13" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$2" x="-10" y="21.59" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$3" x="-10" y="19.05" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$4" x="-10" y="16.51" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$5" x="-10" y="13.97" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$6" x="-10" y="11.43" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$7" x="-10" y="8.89" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$8" x="-10" y="6.35" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$9" x="-10" y="3.81" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$10" x="-10" y="1.27" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$11" x="-10" y="-1.27" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$12" x="-10" y="-3.81" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$13" x="-10" y="-6.35" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$14" x="-10" y="-8.89" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$15" x="-10" y="-11.43" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$16" x="-10" y="-13.97" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$17" x="-10" y="-16.51" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$18" x="-10" y="-19.05" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$19" x="-10" y="-21.59" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$20" x="-10" y="-24.13" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$21" x="10" y="-24.13" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$22" x="10" y="-21.59" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$23" x="10" y="-19.05" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$24" x="10" y="-16.51" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$25" x="10" y="-13.97" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$26" x="10" y="-11.43" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$27" x="10" y="-8.89" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$28" x="10" y="-6.35" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$29" x="10" y="-3.81" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$30" x="10" y="-1.27" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$31" x="10" y="1.27" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$32" x="10" y="3.81" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$33" x="10" y="6.35" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$34" x="10" y="8.89" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$35" x="10" y="11.43" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$36" x="10" y="13.97" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$37" x="10" y="16.51" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$38" x="10" y="19.05" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$39" x="10" y="21.59" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$40" x="10" y="24.13" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<hole x="-2.725" y="24" drill="1.8"/>
<hole x="2.725" y="24" drill="1.8"/>
<hole x="-2.425" y="20.97" drill="1.5"/>
<hole x="2.425" y="20.97" drill="1.5"/>
<polygon width="0.127" layer="41" pour="solid">
<vertex x="-3.5" y="16.5"/>
<vertex x="-1.5" y="16.5"/>
<vertex x="-1.5" y="18.5"/>
<vertex x="-3.5" y="18.5"/>
</polygon>
<polygon width="0.127" layer="41" pour="solid">
<vertex x="-3.5" y="14"/>
<vertex x="-1.5" y="14"/>
<vertex x="-1.5" y="16"/>
<vertex x="-3.5" y="16"/>
</polygon>
<polygon width="0.127" layer="41" pour="solid">
<vertex x="-3.5" y="11.5"/>
<vertex x="-1.5" y="11.5"/>
<vertex x="-1.5" y="13.5"/>
<vertex x="-3.5" y="13.5"/>
</polygon>
<polygon width="0.127" layer="41" pour="solid">
<vertex x="-3.7" y="20.2"/>
<vertex x="3.7" y="20.2"/>
<vertex x="3.7" y="24.9"/>
<vertex x="-3.7" y="24.9"/>
</polygon>
<pad name="41" x="-2.54" y="-23.9" drill="1"/>
<pad name="42" x="0" y="-23.9" drill="1"/>
<pad name="43" x="2.54" y="-23.9" drill="1"/>
<smd name="P$41" x="-2.54" y="-24.925" dx="3.5" dy="1.7" layer="1" rot="R270"/>
<smd name="P$42" x="0" y="-24.925" dx="3.5" dy="1.7" layer="1" rot="R270"/>
<smd name="P$43" x="2.54" y="-24.925" dx="3.5" dy="1.7" layer="1" rot="R270"/>
<circle x="-12.7" y="25.4" radius="0.635" width="0" layer="21"/>
<wire x1="-4" y1="26.8" x2="4" y2="26.8" width="0.127" layer="21"/>
<wire x1="4" y1="26.8" x2="4" y2="20" width="0.127" layer="21"/>
<wire x1="4" y1="20" x2="-4" y2="20" width="0.127" layer="21"/>
<wire x1="-4" y1="20" x2="-4" y2="26.8" width="0.127" layer="21"/>
<wire x1="-10.5" y1="22.09" x2="-10.5" y2="21.09" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="24.63" x2="-10.5" y2="23.63" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="19.55" x2="-10.5" y2="18.55" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="17.01" x2="-10.5" y2="16.01" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="14.47" x2="-10.5" y2="13.47" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="11.93" x2="-10.5" y2="10.93" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="9.39" x2="-10.5" y2="8.39" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="6.85" x2="-10.5" y2="5.85" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="4.31" x2="-10.5" y2="3.31" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="1.77" x2="-10.5" y2="0.77" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-0.77" x2="-10.5" y2="-1.77" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-3.31" x2="-10.5" y2="-4.31" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-5.85" x2="-10.5" y2="-6.85" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-8.39" x2="-10.5" y2="-9.39" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-10.93" x2="-10.5" y2="-11.93" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-13.47" x2="-10.5" y2="-14.47" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-16.01" x2="-10.5" y2="-17.01" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-18.55" x2="-10.5" y2="-19.55" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-21.09" x2="-10.5" y2="-22.09" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-23.63" x2="-10.5" y2="-24.63" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-24.63" x2="10.5" y2="-23.63" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-22.09" x2="10.5" y2="-21.09" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-19.55" x2="10.5" y2="-18.55" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-17.01" x2="10.5" y2="-16.01" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-14.47" x2="10.5" y2="-13.47" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-11.93" x2="10.5" y2="-10.93" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-9.39" x2="10.5" y2="-8.39" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-6.85" x2="10.5" y2="-5.85" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-4.31" x2="10.5" y2="-3.31" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-1.77" x2="10.5" y2="-0.77" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="0.77" x2="10.5" y2="1.77" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="3.31" x2="10.5" y2="4.31" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="5.85" x2="10.5" y2="6.85" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="8.39" x2="10.5" y2="9.39" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="10.93" x2="10.5" y2="11.93" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="13.47" x2="10.5" y2="14.47" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="16.01" x2="10.5" y2="17.01" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="18.55" x2="10.5" y2="19.55" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="21.09" x2="10.5" y2="22.09" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="23.63" x2="10.5" y2="24.63" width="0.127" layer="21" curve="-180"/>
<wire x1="-0.5" y1="-25.5" x2="0.5" y2="-25.5" width="0.127" layer="21" curve="-180"/>
<wire x1="2.04" y1="-25.5" x2="3.04" y2="-25.5" width="0.127" layer="21" curve="-180"/>
<wire x1="-3.04" y1="-25.5" x2="-2.04" y2="-25.5" width="0.127" layer="21" curve="-180"/>
</package>
<package name="PICO-PKG-SMD">
<wire x1="-10.5" y1="25.5" x2="10.5" y2="25.5" width="0.1524" layer="21"/>
<text x="-10.414" y="-28.067" size="1.778" layer="25">&gt;NAME</text>
<text x="1.016" y="-20.955" size="1.778" layer="27" rot="R90">&gt;VALUE</text>
<smd name="P$1" x="-10" y="24.13" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$2" x="-10" y="21.59" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$3" x="-10" y="19.05" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$4" x="-10" y="16.51" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$5" x="-10" y="13.97" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$6" x="-10" y="11.43" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$7" x="-10" y="8.89" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$8" x="-10" y="6.35" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$9" x="-10" y="3.81" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$10" x="-10" y="1.27" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$11" x="-10" y="-1.27" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$12" x="-10" y="-3.81" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$13" x="-10" y="-6.35" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$14" x="-10" y="-8.89" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$15" x="-10" y="-11.43" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$16" x="-10" y="-13.97" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$17" x="-10" y="-16.51" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$18" x="-10" y="-19.05" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$19" x="-10" y="-21.59" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$20" x="-10" y="-24.13" dx="3.5" dy="1.7" layer="1"/>
<smd name="P$21" x="10" y="-24.13" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$22" x="10" y="-21.59" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$23" x="10" y="-19.05" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$24" x="10" y="-16.51" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$25" x="10" y="-13.97" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$26" x="10" y="-11.43" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$27" x="10" y="-8.89" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$28" x="10" y="-6.35" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$29" x="10" y="-3.81" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$30" x="10" y="-1.27" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$31" x="10" y="1.27" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$32" x="10" y="3.81" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$33" x="10" y="6.35" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$34" x="10" y="8.89" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$35" x="10" y="11.43" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$36" x="10" y="13.97" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$37" x="10" y="16.51" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$38" x="10" y="19.05" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$39" x="10" y="21.59" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<smd name="P$40" x="10" y="24.13" dx="3.5" dy="1.7" layer="1" rot="R180"/>
<hole x="-2.725" y="24" drill="1.8"/>
<hole x="2.725" y="24" drill="1.8"/>
<hole x="-2.425" y="20.97" drill="1.5"/>
<hole x="2.425" y="20.97" drill="1.5"/>
<polygon width="0.127" layer="41" pour="solid">
<vertex x="-3.5" y="16.5"/>
<vertex x="-1.5" y="16.5"/>
<vertex x="-1.5" y="18.5"/>
<vertex x="-3.5" y="18.5"/>
</polygon>
<polygon width="0.127" layer="41" pour="solid">
<vertex x="-3.5" y="14"/>
<vertex x="-1.5" y="14"/>
<vertex x="-1.5" y="16"/>
<vertex x="-3.5" y="16"/>
</polygon>
<polygon width="0.127" layer="41" pour="solid">
<vertex x="-3.5" y="11.5"/>
<vertex x="-1.5" y="11.5"/>
<vertex x="-1.5" y="13.5"/>
<vertex x="-3.5" y="13.5"/>
</polygon>
<polygon width="0.127" layer="41" pour="solid">
<vertex x="-3.7" y="20.2"/>
<vertex x="3.7" y="20.2"/>
<vertex x="3.7" y="24.9"/>
<vertex x="-3.7" y="24.9"/>
</polygon>
<smd name="P$41" x="-2.54" y="-24.925" dx="3.5" dy="1.7" layer="1" rot="R270"/>
<smd name="P$42" x="0" y="-24.925" dx="3.5" dy="1.7" layer="1" rot="R270"/>
<smd name="P$43" x="2.54" y="-24.925" dx="3.5" dy="1.7" layer="1" rot="R270"/>
<circle x="-12.7" y="25.4" radius="0.635" width="0" layer="21"/>
<wire x1="-4" y1="26.8" x2="4" y2="26.8" width="0.127" layer="21"/>
<wire x1="4" y1="26.8" x2="4" y2="20" width="0.127" layer="21"/>
<wire x1="4" y1="20" x2="-4" y2="20" width="0.127" layer="21"/>
<wire x1="-4" y1="20" x2="-4" y2="26.8" width="0.127" layer="21"/>
<wire x1="10.5" y1="-25.5" x2="10.5" y2="-24.63" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-23.63" x2="10.5" y2="-22.09" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-21.09" x2="10.5" y2="-19.55" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-18.55" x2="10.5" y2="-17.01" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-16.01" x2="10.5" y2="-14.47" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-13.47" x2="10.5" y2="-11.93" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-10.93" x2="10.5" y2="-9.39" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-8.39" x2="10.5" y2="-6.85" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-5.85" x2="10.5" y2="-4.31" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-3.31" x2="10.5" y2="-1.77" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-0.77" x2="10.5" y2="0.77" width="0.1524" layer="21"/>
<wire x1="10.5" y1="1.77" x2="10.5" y2="3.31" width="0.1524" layer="21"/>
<wire x1="10.5" y1="4.31" x2="10.5" y2="5.85" width="0.1524" layer="21"/>
<wire x1="10.5" y1="6.85" x2="10.5" y2="8.39" width="0.1524" layer="21"/>
<wire x1="10.5" y1="9.39" x2="10.5" y2="10.93" width="0.1524" layer="21"/>
<wire x1="10.5" y1="11.93" x2="10.5" y2="13.47" width="0.1524" layer="21"/>
<wire x1="10.5" y1="14.47" x2="10.5" y2="16.01" width="0.1524" layer="21"/>
<wire x1="10.5" y1="17.01" x2="10.5" y2="18.55" width="0.1524" layer="21"/>
<wire x1="10.5" y1="19.55" x2="10.5" y2="21.09" width="0.1524" layer="21"/>
<wire x1="10.5" y1="22.09" x2="10.5" y2="23.63" width="0.1524" layer="21"/>
<wire x1="10.5" y1="24.63" x2="10.5" y2="25.5" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="25.5" x2="-10.5" y2="24.63" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="23.63" x2="-10.5" y2="22.09" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="21.09" x2="-10.5" y2="19.55" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="18.55" x2="-10.5" y2="17.01" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="16.01" x2="-10.5" y2="14.47" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="13.47" x2="-10.5" y2="11.93" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="10.93" x2="-10.5" y2="9.39" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="8.39" x2="-10.5" y2="6.85" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="5.85" x2="-10.5" y2="4.31" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="3.31" x2="-10.5" y2="1.77" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="0.77" x2="-10.5" y2="-0.77" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-1.77" x2="-10.5" y2="-3.31" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-4.31" x2="-10.5" y2="-5.85" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-6.85" x2="-10.5" y2="-8.39" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-9.39" x2="-10.5" y2="-10.93" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-11.93" x2="-10.5" y2="-13.47" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-14.47" x2="-10.5" y2="-16.01" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-17.01" x2="-10.5" y2="-18.55" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-19.55" x2="-10.5" y2="-21.09" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-22.09" x2="-10.5" y2="-23.63" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-24.63" x2="-10.5" y2="-25.5" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-25.5" x2="3.04" y2="-25.5" width="0.1524" layer="21"/>
<wire x1="2.04" y1="-25.5" x2="0.5" y2="-25.5" width="0.1524" layer="21"/>
<wire x1="-0.5" y1="-25.5" x2="-2.04" y2="-25.5" width="0.1524" layer="21"/>
<wire x1="-3.04" y1="-25.5" x2="-10.5" y2="-25.5" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="22.09" x2="-10.5" y2="21.09" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="24.63" x2="-10.5" y2="23.63" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="19.55" x2="-10.5" y2="18.55" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="17.01" x2="-10.5" y2="16.01" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="14.47" x2="-10.5" y2="13.47" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="11.93" x2="-10.5" y2="10.93" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="9.39" x2="-10.5" y2="8.39" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="6.85" x2="-10.5" y2="5.85" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="4.31" x2="-10.5" y2="3.31" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="1.77" x2="-10.5" y2="0.77" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-0.77" x2="-10.5" y2="-1.77" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-3.31" x2="-10.5" y2="-4.31" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-5.85" x2="-10.5" y2="-6.85" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-8.39" x2="-10.5" y2="-9.39" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-10.93" x2="-10.5" y2="-11.93" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-13.47" x2="-10.5" y2="-14.47" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-16.01" x2="-10.5" y2="-17.01" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-18.55" x2="-10.5" y2="-19.55" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-21.09" x2="-10.5" y2="-22.09" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-23.63" x2="-10.5" y2="-24.63" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-24.63" x2="10.5" y2="-23.63" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-22.09" x2="10.5" y2="-21.09" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-19.55" x2="10.5" y2="-18.55" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-17.01" x2="10.5" y2="-16.01" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-14.47" x2="10.5" y2="-13.47" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-11.93" x2="10.5" y2="-10.93" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-9.39" x2="10.5" y2="-8.39" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-6.85" x2="10.5" y2="-5.85" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-4.31" x2="10.5" y2="-3.31" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-1.77" x2="10.5" y2="-0.77" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="0.77" x2="10.5" y2="1.77" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="3.31" x2="10.5" y2="4.31" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="5.85" x2="10.5" y2="6.85" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="8.39" x2="10.5" y2="9.39" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="10.93" x2="10.5" y2="11.93" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="13.47" x2="10.5" y2="14.47" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="16.01" x2="10.5" y2="17.01" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="18.55" x2="10.5" y2="19.55" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="21.09" x2="10.5" y2="22.09" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="23.63" x2="10.5" y2="24.63" width="0.127" layer="21" curve="-180"/>
<wire x1="-0.5" y1="-25.5" x2="0.5" y2="-25.5" width="0.127" layer="21" curve="-180"/>
<wire x1="2.04" y1="-25.5" x2="3.04" y2="-25.5" width="0.127" layer="21" curve="-180"/>
<wire x1="-3.04" y1="-25.5" x2="-2.04" y2="-25.5" width="0.127" layer="21" curve="-180"/>
</package>
<package name="PICO-PKG-TH">
<wire x1="-10.5" y1="25.5" x2="10.5" y2="25.5" width="0.1524" layer="21"/>
<pad name="1" x="-8.89" y="24.13" drill="1"/>
<pad name="2" x="-8.89" y="21.59" drill="1"/>
<pad name="7" x="-8.89" y="8.89" drill="1"/>
<pad name="8" x="-8.89" y="6.35" drill="1"/>
<pad name="3" x="-8.89" y="19.05" drill="1"/>
<pad name="4" x="-8.89" y="16.51" drill="1"/>
<pad name="6" x="-8.89" y="11.43" drill="1"/>
<pad name="5" x="-8.89" y="13.97" drill="1"/>
<pad name="9" x="-8.89" y="3.81" drill="1"/>
<pad name="10" x="-8.89" y="1.27" drill="1"/>
<pad name="11" x="-8.89" y="-1.27" drill="1"/>
<pad name="12" x="-8.89" y="-3.81" drill="1"/>
<pad name="13" x="-8.89" y="-6.35" drill="1"/>
<pad name="14" x="-8.89" y="-8.89" drill="1"/>
<pad name="15" x="-8.89" y="-11.43" drill="1"/>
<pad name="16" x="-8.89" y="-13.97" drill="1"/>
<pad name="17" x="-8.89" y="-16.51" drill="1"/>
<pad name="18" x="-8.89" y="-19.05" drill="1"/>
<pad name="19" x="-8.89" y="-21.59" drill="1"/>
<pad name="20" x="-8.89" y="-24.13" drill="1"/>
<pad name="21" x="8.89" y="-24.13" drill="1"/>
<pad name="22" x="8.89" y="-21.59" drill="1"/>
<pad name="23" x="8.89" y="-19.05" drill="1"/>
<pad name="24" x="8.89" y="-16.51" drill="1"/>
<pad name="25" x="8.89" y="-13.97" drill="1"/>
<pad name="26" x="8.89" y="-11.43" drill="1"/>
<pad name="27" x="8.89" y="-8.89" drill="1"/>
<pad name="28" x="8.89" y="-6.35" drill="1"/>
<pad name="29" x="8.89" y="-3.81" drill="1"/>
<pad name="30" x="8.89" y="-1.27" drill="1"/>
<pad name="31" x="8.89" y="1.27" drill="1"/>
<pad name="32" x="8.89" y="3.81" drill="1"/>
<pad name="33" x="8.89" y="6.35" drill="1"/>
<pad name="34" x="8.89" y="8.89" drill="1"/>
<pad name="35" x="8.89" y="11.43" drill="1"/>
<pad name="36" x="8.89" y="13.97" drill="1"/>
<pad name="37" x="8.89" y="16.51" drill="1"/>
<pad name="38" x="8.89" y="19.05" drill="1"/>
<pad name="39" x="8.89" y="21.59" drill="1"/>
<pad name="40" x="8.89" y="24.13" drill="1"/>
<text x="-10.414" y="-28.067" size="1.778" layer="25">&gt;NAME</text>
<text x="1.016" y="-20.955" size="1.778" layer="27" rot="R90">&gt;VALUE</text>
<hole x="-2.725" y="24" drill="1.8"/>
<hole x="2.725" y="24" drill="1.8"/>
<hole x="-2.425" y="20.97" drill="1.5"/>
<hole x="2.425" y="20.97" drill="1.5"/>
<polygon width="0.127" layer="41" pour="solid">
<vertex x="-3.5" y="16.5"/>
<vertex x="-1.5" y="16.5"/>
<vertex x="-1.5" y="18.5"/>
<vertex x="-3.5" y="18.5"/>
</polygon>
<polygon width="0.127" layer="41" pour="solid">
<vertex x="-3.5" y="14"/>
<vertex x="-1.5" y="14"/>
<vertex x="-1.5" y="16"/>
<vertex x="-3.5" y="16"/>
</polygon>
<polygon width="0.127" layer="41" pour="solid">
<vertex x="-3.5" y="11.5"/>
<vertex x="-1.5" y="11.5"/>
<vertex x="-1.5" y="13.5"/>
<vertex x="-3.5" y="13.5"/>
</polygon>
<polygon width="0.127" layer="41" pour="solid">
<vertex x="-3.7" y="20.2"/>
<vertex x="3.7" y="20.2"/>
<vertex x="3.7" y="24.9"/>
<vertex x="-3.7" y="24.9"/>
</polygon>
<pad name="41" x="-2.54" y="-23.9" drill="1"/>
<pad name="42" x="0" y="-23.9" drill="1"/>
<pad name="43" x="2.54" y="-23.9" drill="1"/>
<circle x="-12.7" y="25.4" radius="0.635" width="0" layer="21"/>
<wire x1="-4" y1="26.8" x2="4" y2="26.8" width="0.127" layer="21"/>
<wire x1="4" y1="26.8" x2="4" y2="20" width="0.127" layer="21"/>
<wire x1="4" y1="20" x2="-4" y2="20" width="0.127" layer="21"/>
<wire x1="-4" y1="20" x2="-4" y2="26.8" width="0.127" layer="21"/>
<wire x1="10.5" y1="-25.5" x2="10.5" y2="-24.63" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-23.63" x2="10.5" y2="-22.09" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-21.09" x2="10.5" y2="-19.55" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-18.55" x2="10.5" y2="-17.01" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-16.01" x2="10.5" y2="-14.47" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-13.47" x2="10.5" y2="-11.93" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-10.93" x2="10.5" y2="-9.39" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-8.39" x2="10.5" y2="-6.85" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-5.85" x2="10.5" y2="-4.31" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-3.31" x2="10.5" y2="-1.77" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-0.77" x2="10.5" y2="0.77" width="0.1524" layer="21"/>
<wire x1="10.5" y1="1.77" x2="10.5" y2="3.31" width="0.1524" layer="21"/>
<wire x1="10.5" y1="4.31" x2="10.5" y2="5.85" width="0.1524" layer="21"/>
<wire x1="10.5" y1="6.85" x2="10.5" y2="8.39" width="0.1524" layer="21"/>
<wire x1="10.5" y1="9.39" x2="10.5" y2="10.93" width="0.1524" layer="21"/>
<wire x1="10.5" y1="11.93" x2="10.5" y2="13.47" width="0.1524" layer="21"/>
<wire x1="10.5" y1="14.47" x2="10.5" y2="16.01" width="0.1524" layer="21"/>
<wire x1="10.5" y1="17.01" x2="10.5" y2="18.55" width="0.1524" layer="21"/>
<wire x1="10.5" y1="19.55" x2="10.5" y2="21.09" width="0.1524" layer="21"/>
<wire x1="10.5" y1="22.09" x2="10.5" y2="23.63" width="0.1524" layer="21"/>
<wire x1="10.5" y1="24.63" x2="10.5" y2="25.5" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="25.5" x2="-10.5" y2="24.63" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="23.63" x2="-10.5" y2="22.09" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="21.09" x2="-10.5" y2="19.55" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="18.55" x2="-10.5" y2="17.01" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="16.01" x2="-10.5" y2="14.47" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="13.47" x2="-10.5" y2="11.93" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="10.93" x2="-10.5" y2="9.39" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="8.39" x2="-10.5" y2="6.85" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="5.85" x2="-10.5" y2="4.31" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="3.31" x2="-10.5" y2="1.77" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="0.77" x2="-10.5" y2="-0.77" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-1.77" x2="-10.5" y2="-3.31" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-4.31" x2="-10.5" y2="-5.85" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-6.85" x2="-10.5" y2="-8.39" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-9.39" x2="-10.5" y2="-10.93" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-11.93" x2="-10.5" y2="-13.47" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-14.47" x2="-10.5" y2="-16.01" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-17.01" x2="-10.5" y2="-18.55" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-19.55" x2="-10.5" y2="-21.09" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-22.09" x2="-10.5" y2="-23.63" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="-24.63" x2="-10.5" y2="-25.5" width="0.1524" layer="21"/>
<wire x1="10.5" y1="-25.5" x2="3.04" y2="-25.5" width="0.1524" layer="21"/>
<wire x1="2.04" y1="-25.5" x2="0.5" y2="-25.5" width="0.1524" layer="21"/>
<wire x1="-0.5" y1="-25.5" x2="-2.04" y2="-25.5" width="0.1524" layer="21"/>
<wire x1="-3.04" y1="-25.5" x2="-10.5" y2="-25.5" width="0.1524" layer="21"/>
<wire x1="-10.5" y1="22.09" x2="-10.5" y2="21.09" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="24.63" x2="-10.5" y2="23.63" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="19.55" x2="-10.5" y2="18.55" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="17.01" x2="-10.5" y2="16.01" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="14.47" x2="-10.5" y2="13.47" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="11.93" x2="-10.5" y2="10.93" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="9.39" x2="-10.5" y2="8.39" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="6.85" x2="-10.5" y2="5.85" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="4.31" x2="-10.5" y2="3.31" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="1.77" x2="-10.5" y2="0.77" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-0.77" x2="-10.5" y2="-1.77" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-3.31" x2="-10.5" y2="-4.31" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-5.85" x2="-10.5" y2="-6.85" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-8.39" x2="-10.5" y2="-9.39" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-10.93" x2="-10.5" y2="-11.93" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-13.47" x2="-10.5" y2="-14.47" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-16.01" x2="-10.5" y2="-17.01" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-18.55" x2="-10.5" y2="-19.55" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-21.09" x2="-10.5" y2="-22.09" width="0.127" layer="21" curve="-180"/>
<wire x1="-10.5" y1="-23.63" x2="-10.5" y2="-24.63" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-24.63" x2="10.5" y2="-23.63" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-22.09" x2="10.5" y2="-21.09" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-19.55" x2="10.5" y2="-18.55" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-17.01" x2="10.5" y2="-16.01" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-14.47" x2="10.5" y2="-13.47" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-11.93" x2="10.5" y2="-10.93" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-9.39" x2="10.5" y2="-8.39" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-6.85" x2="10.5" y2="-5.85" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-4.31" x2="10.5" y2="-3.31" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="-1.77" x2="10.5" y2="-0.77" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="0.77" x2="10.5" y2="1.77" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="3.31" x2="10.5" y2="4.31" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="5.85" x2="10.5" y2="6.85" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="8.39" x2="10.5" y2="9.39" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="10.93" x2="10.5" y2="11.93" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="13.47" x2="10.5" y2="14.47" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="16.01" x2="10.5" y2="17.01" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="18.55" x2="10.5" y2="19.55" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="21.09" x2="10.5" y2="22.09" width="0.127" layer="21" curve="-180"/>
<wire x1="10.5" y1="23.63" x2="10.5" y2="24.63" width="0.127" layer="21" curve="-180"/>
<wire x1="-0.5" y1="-25.5" x2="0.5" y2="-25.5" width="0.127" layer="21" curve="-180"/>
<wire x1="2.04" y1="-25.5" x2="3.04" y2="-25.5" width="0.127" layer="21" curve="-180"/>
<wire x1="-3.04" y1="-25.5" x2="-2.04" y2="-25.5" width="0.127" layer="21" curve="-180"/>
</package>
</packages>
<symbols>
<symbol name="PICO-SYM">
<pin name="GP0" x="-17.78" y="25.4" length="middle"/>
<pin name="GP1" x="-17.78" y="22.86" length="middle"/>
<pin name="GP2" x="-17.78" y="17.78" length="middle"/>
<pin name="GP3" x="-17.78" y="15.24" length="middle"/>
<pin name="GP4" x="-17.78" y="12.7" length="middle"/>
<pin name="GP5" x="-17.78" y="10.16" length="middle"/>
<pin name="GP6" x="-17.78" y="5.08" length="middle"/>
<pin name="GP7" x="-17.78" y="2.54" length="middle"/>
<pin name="GP8" x="-17.78" y="0" length="middle"/>
<pin name="GP9" x="-17.78" y="-2.54" length="middle"/>
<pin name="GP10" x="-17.78" y="-7.62" length="middle"/>
<pin name="GP11" x="-17.78" y="-10.16" length="middle"/>
<pin name="GP12" x="-17.78" y="-12.7" length="middle"/>
<pin name="GP13" x="-17.78" y="-15.24" length="middle"/>
<pin name="GP14" x="-17.78" y="-20.32" length="middle"/>
<pin name="GP15" x="-17.78" y="-22.86" length="middle"/>
<pin name="GP16" x="17.78" y="-22.86" length="middle" rot="R180"/>
<pin name="GP17" x="17.78" y="-20.32" length="middle" rot="R180"/>
<pin name="GP18" x="17.78" y="-15.24" length="middle" rot="R180"/>
<pin name="GP19" x="17.78" y="-12.7" length="middle" rot="R180"/>
<pin name="GP20" x="17.78" y="-10.16" length="middle" rot="R180"/>
<pin name="GP21" x="17.78" y="-7.62" length="middle" rot="R180"/>
<pin name="GP22" x="17.78" y="-2.54" length="middle" rot="R180"/>
<pin name="RUN" x="17.78" y="22.86" length="middle" direction="in" rot="R180"/>
<pin name="GP26" x="17.78" y="2.54" length="middle" rot="R180"/>
<pin name="GP27" x="17.78" y="5.08" length="middle" rot="R180"/>
<pin name="GP28" x="17.78" y="10.16" length="middle" rot="R180"/>
<pin name="ADC_REF" x="17.78" y="17.78" length="middle" direction="in" rot="R180"/>
<pin name="3V3(OUT)" x="17.78" y="30.48" length="middle" direction="pwr" rot="R180"/>
<pin name="3V3_EN" x="17.78" y="25.4" length="middle" direction="in" rot="R180"/>
<pin name="GND" x="17.78" y="-35.56" length="middle" direction="pwr" rot="R180"/>
<pin name="VSYS" x="17.78" y="33.02" length="middle" direction="pwr" rot="R180"/>
<pin name="VBUS" x="17.78" y="35.56" length="middle" direction="pwr" rot="R180"/>
<wire x1="-12.7" y1="38.1" x2="12.7" y2="38.1" width="0.254" layer="94"/>
<wire x1="12.7" y1="38.1" x2="12.7" y2="-38.1" width="0.254" layer="94"/>
<wire x1="12.7" y1="-38.1" x2="-12.7" y2="-38.1" width="0.254" layer="94"/>
<wire x1="-12.7" y1="-38.1" x2="-12.7" y2="38.1" width="0.254" layer="94"/>
<text x="-12.7155" y="39.4146" size="2.54388125" layer="95">&gt;NAME</text>
<text x="-12.7069" y="-41.9314" size="2.54171875" layer="96">&gt;VALUE</text>
<pin name="SWDIO" x="-17.78" y="-35.56" length="middle"/>
<pin name="SWGND" x="-17.78" y="-33.02" length="middle" direction="pwr"/>
<pin name="SWCLK" x="-17.78" y="-30.48" length="middle" direction="in"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="RASPBERRY_PICO" prefix="U">
<description>Raspberry Pi Pico</description>
<gates>
<gate name="U$1" symbol="PICO-SYM" x="0" y="-20.32"/>
</gates>
<devices>
<device name="SMD-TH" package="PICO-PKG">
<connects>
<connect gate="U$1" pin="3V3(OUT)" pad="36 P$36"/>
<connect gate="U$1" pin="3V3_EN" pad="37 P$37"/>
<connect gate="U$1" pin="ADC_REF" pad="35 P$35"/>
<connect gate="U$1" pin="GND" pad="3 8 13 18 23 28 33 38 P$3 P$8 P$13 P$18 P$23 P$28 P$33 P$38"/>
<connect gate="U$1" pin="GP0" pad="1 P$1"/>
<connect gate="U$1" pin="GP1" pad="2 P$2"/>
<connect gate="U$1" pin="GP10" pad="14 P$14"/>
<connect gate="U$1" pin="GP11" pad="15 P$15"/>
<connect gate="U$1" pin="GP12" pad="16 P$16"/>
<connect gate="U$1" pin="GP13" pad="17 P$17"/>
<connect gate="U$1" pin="GP14" pad="19 P$19"/>
<connect gate="U$1" pin="GP15" pad="20 P$20"/>
<connect gate="U$1" pin="GP16" pad="21 P$21"/>
<connect gate="U$1" pin="GP17" pad="22 P$22"/>
<connect gate="U$1" pin="GP18" pad="24 P$24"/>
<connect gate="U$1" pin="GP19" pad="25 P$25"/>
<connect gate="U$1" pin="GP2" pad="4 P$4"/>
<connect gate="U$1" pin="GP20" pad="26 P$26"/>
<connect gate="U$1" pin="GP21" pad="27 P$27"/>
<connect gate="U$1" pin="GP22" pad="29 P$29"/>
<connect gate="U$1" pin="GP26" pad="31 P$31"/>
<connect gate="U$1" pin="GP27" pad="32 P$32"/>
<connect gate="U$1" pin="GP28" pad="34 P$34"/>
<connect gate="U$1" pin="GP3" pad="5 P$5"/>
<connect gate="U$1" pin="GP4" pad="6 P$6"/>
<connect gate="U$1" pin="GP5" pad="7 P$7"/>
<connect gate="U$1" pin="GP6" pad="9 P$9"/>
<connect gate="U$1" pin="GP7" pad="10 P$10"/>
<connect gate="U$1" pin="GP8" pad="11 P$11"/>
<connect gate="U$1" pin="GP9" pad="12 P$12"/>
<connect gate="U$1" pin="RUN" pad="30 P$30"/>
<connect gate="U$1" pin="SWCLK" pad="41 P$41"/>
<connect gate="U$1" pin="SWDIO" pad="43 P$43"/>
<connect gate="U$1" pin="SWGND" pad="42 P$42"/>
<connect gate="U$1" pin="VBUS" pad="40 P$40"/>
<connect gate="U$1" pin="VSYS" pad="39 P$39"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
<device name="SMD" package="PICO-PKG-SMD">
<connects>
<connect gate="U$1" pin="3V3(OUT)" pad="P$36"/>
<connect gate="U$1" pin="3V3_EN" pad="P$37"/>
<connect gate="U$1" pin="ADC_REF" pad="P$35"/>
<connect gate="U$1" pin="GND" pad="P$3 P$8 P$13 P$18 P$23 P$28 P$33 P$38"/>
<connect gate="U$1" pin="GP0" pad="P$1"/>
<connect gate="U$1" pin="GP1" pad="P$2"/>
<connect gate="U$1" pin="GP10" pad="P$14"/>
<connect gate="U$1" pin="GP11" pad="P$15"/>
<connect gate="U$1" pin="GP12" pad="P$16"/>
<connect gate="U$1" pin="GP13" pad="P$17"/>
<connect gate="U$1" pin="GP14" pad="P$19"/>
<connect gate="U$1" pin="GP15" pad="P$20"/>
<connect gate="U$1" pin="GP16" pad="P$21"/>
<connect gate="U$1" pin="GP17" pad="P$22"/>
<connect gate="U$1" pin="GP18" pad="P$24"/>
<connect gate="U$1" pin="GP19" pad="P$25"/>
<connect gate="U$1" pin="GP2" pad="P$4"/>
<connect gate="U$1" pin="GP20" pad="P$26"/>
<connect gate="U$1" pin="GP21" pad="P$27"/>
<connect gate="U$1" pin="GP22" pad="P$29"/>
<connect gate="U$1" pin="GP26" pad="P$31"/>
<connect gate="U$1" pin="GP27" pad="P$32"/>
<connect gate="U$1" pin="GP28" pad="P$34"/>
<connect gate="U$1" pin="GP3" pad="P$5"/>
<connect gate="U$1" pin="GP4" pad="P$6"/>
<connect gate="U$1" pin="GP5" pad="P$7"/>
<connect gate="U$1" pin="GP6" pad="P$9"/>
<connect gate="U$1" pin="GP7" pad="P$10"/>
<connect gate="U$1" pin="GP8" pad="P$11"/>
<connect gate="U$1" pin="GP9" pad="P$12"/>
<connect gate="U$1" pin="RUN" pad="P$30"/>
<connect gate="U$1" pin="SWCLK" pad="P$41"/>
<connect gate="U$1" pin="SWDIO" pad="P$43"/>
<connect gate="U$1" pin="SWGND" pad="P$42"/>
<connect gate="U$1" pin="VBUS" pad="P$40"/>
<connect gate="U$1" pin="VSYS" pad="P$39"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
<device name="TH" package="PICO-PKG-TH">
<connects>
<connect gate="U$1" pin="3V3(OUT)" pad="36"/>
<connect gate="U$1" pin="3V3_EN" pad="37"/>
<connect gate="U$1" pin="ADC_REF" pad="35"/>
<connect gate="U$1" pin="GND" pad="3 8 13 18 23 28 33 38"/>
<connect gate="U$1" pin="GP0" pad="1"/>
<connect gate="U$1" pin="GP1" pad="2"/>
<connect gate="U$1" pin="GP10" pad="14"/>
<connect gate="U$1" pin="GP11" pad="15"/>
<connect gate="U$1" pin="GP12" pad="16"/>
<connect gate="U$1" pin="GP13" pad="17"/>
<connect gate="U$1" pin="GP14" pad="19"/>
<connect gate="U$1" pin="GP15" pad="20"/>
<connect gate="U$1" pin="GP16" pad="21"/>
<connect gate="U$1" pin="GP17" pad="22"/>
<connect gate="U$1" pin="GP18" pad="24"/>
<connect gate="U$1" pin="GP19" pad="25"/>
<connect gate="U$1" pin="GP2" pad="4"/>
<connect gate="U$1" pin="GP20" pad="26"/>
<connect gate="U$1" pin="GP21" pad="27"/>
<connect gate="U$1" pin="GP22" pad="29"/>
<connect gate="U$1" pin="GP26" pad="31"/>
<connect gate="U$1" pin="GP27" pad="32"/>
<connect gate="U$1" pin="GP28" pad="34"/>
<connect gate="U$1" pin="GP3" pad="5"/>
<connect gate="U$1" pin="GP4" pad="6"/>
<connect gate="U$1" pin="GP5" pad="7"/>
<connect gate="U$1" pin="GP6" pad="9"/>
<connect gate="U$1" pin="GP7" pad="10"/>
<connect gate="U$1" pin="GP8" pad="11"/>
<connect gate="U$1" pin="GP9" pad="12"/>
<connect gate="U$1" pin="RUN" pad="30"/>
<connect gate="U$1" pin="SWCLK" pad="41"/>
<connect gate="U$1" pin="SWDIO" pad="43"/>
<connect gate="U$1" pin="SWGND" pad="42"/>
<connect gate="U$1" pin="VBUS" pad="40"/>
<connect gate="U$1" pin="VSYS" pad="39"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="Terminal Blocks" urn="urn:adsk.eagle:library:11886498">
<description>&lt;h3&gt; PCBLayout.com - Frequently Used &lt;i&gt;Terminal Blocks&lt;/i&gt;&lt;/h3&gt;

Visit us at &lt;a href="http://www.PCBLayout.com"&gt;PCBLayout.com&lt;/a&gt; for quick and hassle-free PCB Layout/Manufacturing ordering experience.
&lt;BR&gt;
&lt;BR&gt;
This library has been generated by our experienced pcb layout engineers using current IPC and/or industry standards. We &lt;b&gt;believe&lt;/b&gt; the content to be accurate, complete and current. But, this content is provided as a courtesy and &lt;u&gt;user assumes all risk and responsiblity of it's usage&lt;/u&gt;.
&lt;BR&gt;
&lt;BR&gt;
Feel free to contact us at &lt;a href="mailto:Support@PCBLayout.com"&gt;Support@PCBLayout.com&lt;/a&gt; if you have any questions/concerns regarding any of our content or services.</description>
<packages>
<package name="TERMINALBLOCK_PLUGGABLE-6-7.62MM" urn="urn:adsk.eagle:footprint:11836841/1" library_version="1">
<text x="-22.16" y="6.27" size="1.778" layer="25">&gt;NAME</text>
<text x="-22.7" y="-7.16" size="1.778" layer="27">&gt;VALUE</text>
<pad name="1" x="-19.05" y="0" drill="1.6" diameter="3.81" shape="square"/>
<pad name="2" x="-11.43" y="0" drill="1.6" diameter="3.81"/>
<pad name="3" x="-3.81" y="0" drill="1.6" diameter="3.81"/>
<pad name="4" x="3.81" y="0" drill="1.6" diameter="3.81"/>
<pad name="5" x="11.43" y="0" drill="1.6" diameter="3.81"/>
<pad name="6" x="19.05" y="0" drill="1.6" diameter="3.81"/>
<wire x1="-22.85" y1="4.3" x2="-22.85" y2="-3.8" width="0.127" layer="21"/>
<wire x1="-22.85" y1="-3.8" x2="22.85" y2="-3.8" width="0.127" layer="21"/>
<wire x1="22.85" y1="-3.8" x2="22.85" y2="4.3" width="0.127" layer="21"/>
<wire x1="22.85" y1="4.3" x2="-22.85" y2="4.3" width="0.127" layer="21"/>
<wire x1="-22.85" y1="4.3" x2="-22.85" y2="-3.8" width="0.127" layer="51"/>
<wire x1="-22.85" y1="-3.8" x2="22.85" y2="-3.8" width="0.127" layer="51"/>
<wire x1="22.85" y1="-3.8" x2="22.85" y2="4.3" width="0.127" layer="51"/>
<wire x1="22.85" y1="4.3" x2="-22.85" y2="4.3" width="0.127" layer="51"/>
<wire x1="-23.1" y1="4.55" x2="-23.1" y2="-4.05" width="0.05" layer="39"/>
<wire x1="-23.1" y1="-4.05" x2="23.1" y2="-4.05" width="0.05" layer="39"/>
<wire x1="23.1" y1="-4.05" x2="23.1" y2="4.55" width="0.05" layer="39"/>
<wire x1="23.1" y1="4.55" x2="-23.1" y2="4.55" width="0.05" layer="39"/>
<circle x="-19.04" y="-4.3" radius="0.2" width="0.4" layer="21"/>
</package>
</packages>
<packages3d>
<package3d name="TERMINALBLOCK_PLUGGABLE-6-7.62MM" urn="urn:adsk.eagle:package:11836875/2" type="model">
<packageinstances>
<packageinstance name="TERMINALBLOCK_PLUGGABLE-6-7.62MM"/>
</packageinstances>
</package3d>
</packages3d>
<symbols>
<symbol name="691311400106" urn="urn:adsk.eagle:symbol:11836857/1" library_version="1">
<pin name="1" x="7.62" y="5.08" length="middle" direction="pas" rot="R180"/>
<pin name="2" x="7.62" y="2.54" length="middle" direction="pas" rot="R180"/>
<pin name="3" x="7.62" y="0" length="middle" direction="pas" rot="R180"/>
<pin name="4" x="7.62" y="-2.54" length="middle" direction="pas" rot="R180"/>
<pin name="5" x="7.62" y="-5.08" length="middle" direction="pas" rot="R180"/>
<pin name="6" x="7.62" y="-7.62" length="middle" direction="pas" rot="R180"/>
<wire x1="2.54" y1="7.62" x2="2.54" y2="-10.16" width="0.254" layer="94"/>
<wire x1="2.54" y1="-10.16" x2="-2.54" y2="-10.16" width="0.254" layer="94"/>
<wire x1="-2.54" y1="-10.16" x2="-2.54" y2="7.62" width="0.254" layer="94"/>
<wire x1="-2.54" y1="7.62" x2="2.54" y2="7.62" width="0.254" layer="94"/>
<text x="-2.54" y="10.16" size="1.778" layer="95">&gt;NAME</text>
<text x="-2.54" y="-12.7" size="1.778" layer="96">&gt;VALUE</text>
</symbol>
</symbols>
<devicesets>
<deviceset name="691311400106" urn="urn:adsk.eagle:component:11836891/2" prefix="J" library_version="1">
<description>&lt;h3&gt; 7.62MM CLOSE VERTICAL PCB HEADER
WR-TBL &lt;/h3&gt;
&lt;BR&gt;
&lt;a href="https://katalog.we-online.com/em/datasheet/6913114001xx.pdf"&gt; Manufacturer's datasheet&lt;/a&gt;</description>
<gates>
<gate name="G$1" symbol="691311400106" x="0" y="0"/>
</gates>
<devices>
<device name="" package="TERMINALBLOCK_PLUGGABLE-6-7.62MM">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
<connect gate="G$1" pin="3" pad="3"/>
<connect gate="G$1" pin="4" pad="4"/>
<connect gate="G$1" pin="5" pad="5"/>
<connect gate="G$1" pin="6" pad="6"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:11836875/2"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="CREATED_BY" value="PCBLayout.com" constant="no"/>
<attribute name="DIGIKEY_PART_NO" value="732-2827-ND" constant="no"/>
<attribute name="MANUFACTURER" value="WURTH ELEKTRONIK" constant="no"/>
<attribute name="MPN" value="691311400106" constant="no"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="Connector">
<description>&lt;b&gt;Pin Headers,Terminal blocks, D-Sub, Backplane, FFC/FPC, Socket</description>
<packages>
<package name="TERMBLK_508-2N" urn="urn:adsk.eagle:footprint:24957600/1">
<pad name="1" x="0" y="0" drill="1.2"/>
<pad name="2" x="5.08" y="0" drill="1.2"/>
<wire x1="7.745" y1="4.25" x2="7.745" y2="-4.25" width="0.1524" layer="21"/>
<wire x1="7.745" y1="-4.25" x2="-2.665" y2="-4.25" width="0.1524" layer="21"/>
<wire x1="-2.665" y1="-4.25" x2="-2.665" y2="4.25" width="0.1524" layer="21"/>
<wire x1="-2.665" y1="4.25" x2="7.745" y2="4.25" width="0.1524" layer="21"/>
<text x="2.54" y="-6.1" size="1.778" layer="25" align="bottom-center">&gt;NAME</text>
<text x="2.54" y="4.6" size="1.778" layer="27" align="bottom-center">&gt;VALUE</text>
</package>
<package name="TERMBLK_254-2N" urn="urn:adsk.eagle:footprint:24957601/1">
<pad name="1" x="0" y="0" drill="1.2"/>
<pad name="2" x="2.54" y="0" drill="1.2"/>
<wire x1="4.165" y1="3.4" x2="4.165" y2="-3.4" width="0.1524" layer="21"/>
<wire x1="4.165" y1="-3.4" x2="-1.625" y2="-3.4" width="0.1524" layer="21"/>
<wire x1="-1.625" y1="-3.4" x2="-1.625" y2="3.4" width="0.1524" layer="21"/>
<wire x1="-1.625" y1="3.4" x2="4.165" y2="3.4" width="0.1524" layer="21"/>
<text x="1.27" y="-5.4" size="1.778" layer="25" align="bottom-center">&gt;NAME</text>
<text x="1.27" y="3.9" size="1.778" layer="27" align="bottom-center">&gt;VALUE</text>
</package>
<package name="TERMBLK_254-3N" urn="urn:adsk.eagle:footprint:24957598/1">
<pad name="1" x="0" y="0" drill="1.2"/>
<pad name="3" x="5.08" y="0" drill="1.2"/>
<pad name="2" x="2.54" y="0" drill="1.2"/>
<wire x1="6.705" y1="3.4" x2="6.705" y2="-3.4" width="0.1524" layer="21"/>
<wire x1="6.705" y1="-3.4" x2="-1.625" y2="-3.4" width="0.1524" layer="21"/>
<wire x1="-1.625" y1="-3.4" x2="-1.625" y2="3.4" width="0.1524" layer="21"/>
<wire x1="-1.625" y1="3.4" x2="6.705" y2="3.4" width="0.1524" layer="21"/>
<text x="2.54" y="-5.4" size="1.778" layer="25" align="bottom-center">&gt;NAME</text>
<text x="2.54" y="3.9" size="1.778" layer="27" align="bottom-center">&gt;VALUE</text>
</package>
<package name="TERMBLK_508-3N" urn="urn:adsk.eagle:footprint:24957599/1">
<pad name="1" x="0" y="0" drill="1.2"/>
<pad name="2" x="5.08" y="0" drill="1.2"/>
<pad name="3" x="10.16" y="0" drill="1.2"/>
<wire x1="12.825" y1="4.25" x2="12.825" y2="-4.25" width="0.1524" layer="21"/>
<wire x1="12.825" y1="-4.25" x2="-2.665" y2="-4.25" width="0.1524" layer="21"/>
<wire x1="-2.665" y1="-4.25" x2="-2.665" y2="4.25" width="0.1524" layer="21"/>
<wire x1="-2.665" y1="4.25" x2="12.825" y2="4.25" width="0.1524" layer="21"/>
<text x="5.08" y="-6.1" size="1.778" layer="25" align="bottom-center">&gt;NAME</text>
<text x="5.08" y="4.6" size="1.778" layer="27" align="bottom-center">&gt;VALUE</text>
</package>
</packages>
<packages3d>
<package3d name="TERMBLK_508-2N" urn="urn:adsk.eagle:package:24957621/1" type="model">
<packageinstances>
<packageinstance name="TERMBLK_508-2N"/>
</packageinstances>
</package3d>
<package3d name="TERMBLK_254-2N" urn="urn:adsk.eagle:package:24957623/1" type="model">
<packageinstances>
<packageinstance name="TERMBLK_254-2N"/>
</packageinstances>
</package3d>
<package3d name="TERMBLK_254-3N" urn="urn:adsk.eagle:package:24957619/1" type="model">
<packageinstances>
<packageinstance name="TERMBLK_254-3N"/>
</packageinstances>
</package3d>
<package3d name="TERMBLK_508-3N" urn="urn:adsk.eagle:package:24957620/1" type="model">
<packageinstances>
<packageinstance name="TERMBLK_508-3N"/>
</packageinstances>
</package3d>
</packages3d>
<symbols>
<symbol name="TERMBLK_2" urn="urn:adsk.eagle:symbol:24957587/3">
<pin name="1" x="-5.08" y="2.54" length="short"/>
<pin name="2" x="-5.08" y="0" length="short"/>
<text x="0" y="-2.794" size="1.778" layer="96" align="top-center">&gt;VALUE</text>
<text x="0" y="5.334" size="1.778" layer="95" align="bottom-center">&gt;NAME</text>
<wire x1="-2.54" y1="-2.54" x2="-2.54" y2="5.08" width="0.1524" layer="94"/>
<wire x1="-2.54" y1="5.08" x2="2.54" y2="5.08" width="0.1524" layer="94"/>
<wire x1="2.54" y1="5.08" x2="2.54" y2="-2.54" width="0.1524" layer="94"/>
<wire x1="2.54" y1="-2.54" x2="-2.54" y2="-2.54" width="0.1524" layer="94"/>
</symbol>
<symbol name="TERMBLK_3" urn="urn:adsk.eagle:symbol:24957588/3">
<pin name="1" x="-5.08" y="2.54" length="short"/>
<pin name="2" x="-5.08" y="0" length="short"/>
<pin name="3" x="-5.08" y="-2.54" length="short"/>
<text x="0" y="-5.334" size="1.778" layer="96" align="top-center">&gt;VALUE</text>
<text x="0" y="5.334" size="1.778" layer="95" align="bottom-center">&gt;NAME</text>
<wire x1="-2.54" y1="5.08" x2="-2.54" y2="-5.08" width="0.1524" layer="94"/>
<wire x1="-2.54" y1="-5.08" x2="2.54" y2="-5.08" width="0.1524" layer="94"/>
<wire x1="2.54" y1="-5.08" x2="2.54" y2="5.08" width="0.1524" layer="94"/>
<wire x1="2.54" y1="5.08" x2="-2.54" y2="5.08" width="0.1524" layer="94"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="2828XX-2" urn="urn:adsk.eagle:component:24957692/5" prefix="J">
<description>2 Position Wire to Board Terminal Block Horizontal with Board
&lt;br&gt;&lt;a href="https://www.te.com.cn/commerce/DocumentDelivery/DDEController?Action=showdoc&amp;DocId=Catalog+Section%7F1308389_EUROSTYLE_TERMINAL_BLOCKS%7F0607%7Fpdf%7FEnglish%7FENG_CS_1308389_EUROSTYLE_TERMINAL_BLOCKS_0607.pdf%7F2-282837-5"&gt;Datasheet&lt;/a&gt;&lt;br&gt;</description>
<gates>
<gate name="G$1" symbol="TERMBLK_2" x="0" y="0"/>
</gates>
<devices>
<device name="282837-2" package="TERMBLK_508-2N">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:24957621/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="CATEGORY" value="Fixed Terminal Blocks" constant="no"/>
<attribute name="DESCRIPTION" value="Fixed Terminal Blocks 5.08MM PCB MOUNT 2P" constant="no"/>
<attribute name="MANUFACTURER" value="TE Connectivity AMP Connectors" constant="no"/>
<attribute name="MPN" value="282837-2" constant="no"/>
<attribute name="OPERATING_TEMPERATURE" value="-40°C to +105°C" constant="no"/>
<attribute name="PART_STATUS" value="ACTIVE" constant="no"/>
<attribute name="PITCH" value="0.200&quot; (5.08mm)" constant="no"/>
<attribute name="ROHS_COMPLIANCE" value="RoHS Compliant" constant="no"/>
<attribute name="SERIES" value="Buchanan" constant="no"/>
<attribute name="SUBCATEGORY" value="Terminal Blocks" constant="no"/>
<attribute name="TYPE" value="Through Hole; Screw - Rising Cage Clamp; Side wire entry, Horizontal with Board" constant="no"/>
</technology>
</technologies>
</device>
<device name="282834-2" package="TERMBLK_254-2N">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:24957623/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="CATEGORY" value="Fixed Terminal Blocks" constant="no"/>
<attribute name="DESCRIPTION" value="Fixed Terminal Blocks 2P SIDE ENTRY 2.54mm" constant="no"/>
<attribute name="MANUFACTURER" value="TE Connectivity AMP Connectors" constant="no"/>
<attribute name="MPN" value="282834-2 " constant="no"/>
<attribute name="OPERATING_TEMPERATURE" value="-40°C ~ 105°C " constant="no"/>
<attribute name="PART_STATUS" value="Active " constant="no"/>
<attribute name="PITCH" value="0.100&quot; (2.54mm) " constant="no"/>
<attribute name="ROHS_COMPLIANCE" value="RoHS Compliant " constant="no"/>
<attribute name="SERIES" value="Buchanan" constant="no"/>
<attribute name="SUBCATEGORY" value="Terminal Blocks " constant="no"/>
<attribute name="TYPE" value="Through Hole; Screw - Rising Cage Clamp; Side wire entry, Horizontal with Board " constant="no"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="2828XX-3" urn="urn:adsk.eagle:component:24957693/5" prefix="J">
<description>3 Position Wire to Board Terminal Block Horizontal with Board
&lt;br&gt;&lt;a href="https://www.te.com.cn/commerce/DocumentDelivery/DDEController?Action=showdoc&amp;DocId=Catalog+Section%7F1308389_EUROSTYLE_TERMINAL_BLOCKS%7F0607%7Fpdf%7FEnglish%7FENG_CS_1308389_EUROSTYLE_TERMINAL_BLOCKS_0607.pdf%7F2-282837-5"&gt;Datasheet&lt;/a&gt;&lt;br&gt;</description>
<gates>
<gate name="G$1" symbol="TERMBLK_3" x="0" y="0"/>
</gates>
<devices>
<device name="282834-3" package="TERMBLK_254-3N">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
<connect gate="G$1" pin="3" pad="3"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:24957619/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="CATEGORY" value="Fixed Terminal Blocks" constant="no"/>
<attribute name="DESCRIPTION" value="Fixed Terminal Blocks 3P TERMINAL BLOCK" constant="no"/>
<attribute name="MANUFACTURER" value="TE Connectivity AMP Connectors" constant="no"/>
<attribute name="MPN" value="282834-3" constant="no"/>
<attribute name="OPERATING_TEMPERATURE" value="-40°C ~ 105°C" constant="no"/>
<attribute name="PART_STATUS" value="Active" constant="no"/>
<attribute name="PITCH" value="0.100&quot; (2.54mm)" constant="no"/>
<attribute name="ROHS_COMPLIANCE" value="RoHS Compliant" constant="no"/>
<attribute name="SERIES" value="Buchanan" constant="no"/>
<attribute name="SUBCATEGORY" value="Terminal Blocks" constant="no"/>
<attribute name="TYPE" value="Through Hole; Screw - Rising Cage Clamp; Side wire entry, Horizontal with Board" constant="no"/>
</technology>
</technologies>
</device>
<device name="282837-3" package="TERMBLK_508-3N">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
<connect gate="G$1" pin="3" pad="3"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:24957620/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="CATEGORY" value="Connector" constant="no"/>
<attribute name="DESCRIPTION" value="TERM BLK 3P SIDE ENT 5.08mm PCB" constant="no"/>
<attribute name="MANUFACTURER" value="TE Connectivity" constant="no"/>
<attribute name="MPN" value="282837-3" constant="no"/>
<attribute name="OPERATING_TEMPERATURE" value="-40°C to +105°C" constant="no"/>
<attribute name="PART_STATUS" value="Active" constant="no"/>
<attribute name="PITCH" value="0.200&quot; (5.08mm)" constant="no"/>
<attribute name="ROHS_COMPLIANCE" value="RoHS Compliant" constant="no"/>
<attribute name="SERIES" value="Buchanan" constant="no"/>
<attribute name="SUBCATEGORY" value="Terminal Block" constant="no"/>
<attribute name="TYPE" value="Side Wire Entry" constant="no"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="Diode">
<description>&lt;B&gt;PN Junction, BridgeRectifier, Zener, Schottky, Switching</description>
<packages>
<package name="DIOMELF3516" urn="urn:adsk.eagle:footprint:16378178/3">
<description>MELF, 3.50 mm length, 1.65 mm diameter
&lt;p&gt;MELF Diode package with 3.50 mm length and 1.65 mm diameter&lt;/p&gt;</description>
<wire x1="0.983" y1="1.239" x2="-2.5717" y2="1.239" width="0.12" layer="21"/>
<wire x1="-2.5717" y1="1.239" x2="-2.5717" y2="-1.239" width="0.12" layer="21"/>
<wire x1="-2.5717" y1="-1.239" x2="0.983" y2="-1.239" width="0.12" layer="21"/>
<wire x1="1.85" y1="-0.85" x2="-1.85" y2="-0.85" width="0.12" layer="51"/>
<wire x1="-1.85" y1="-0.85" x2="-1.85" y2="0.85" width="0.12" layer="51"/>
<wire x1="-1.85" y1="0.85" x2="1.85" y2="0.85" width="0.12" layer="51"/>
<wire x1="1.85" y1="0.85" x2="1.85" y2="-0.85" width="0.12" layer="51"/>
<smd name="1" x="-1.6203" y="0" dx="1.2747" dy="1.85" layer="1"/>
<smd name="2" x="1.6203" y="0" dx="1.2747" dy="1.85" layer="1"/>
<text x="0" y="1.874" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-1.874" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="DIOMELF5024" urn="urn:adsk.eagle:footprint:16378176/3">
<description>MELF, 5.00 mm length, 2.49 mm diameter
&lt;p&gt;MELF Diode package with 5.00 mm length and 2.49 mm diameter&lt;/p&gt;</description>
<wire x1="1.8515" y1="1.659" x2="-3.3217" y2="1.659" width="0.12" layer="21"/>
<wire x1="-3.3217" y1="1.659" x2="-3.3217" y2="-1.659" width="0.12" layer="21"/>
<wire x1="-3.3217" y1="-1.659" x2="1.8515" y2="-1.659" width="0.12" layer="21"/>
<wire x1="2.6" y1="-1.27" x2="-2.6" y2="-1.27" width="0.12" layer="51"/>
<wire x1="-2.6" y1="-1.27" x2="-2.6" y2="1.27" width="0.12" layer="51"/>
<wire x1="-2.6" y1="1.27" x2="2.6" y2="1.27" width="0.12" layer="51"/>
<wire x1="2.6" y1="1.27" x2="2.6" y2="-1.27" width="0.12" layer="51"/>
<smd name="1" x="-2.4296" y="0" dx="1.1561" dy="2.69" layer="1"/>
<smd name="2" x="2.4296" y="0" dx="1.1561" dy="2.69" layer="1"/>
<text x="0" y="2.294" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-2.294" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="SOD3715X135" urn="urn:adsk.eagle:footprint:9427064/1">
<description>SOD, 3.70 mm span, 2.70 X 1.55 X 1.35 mm body
&lt;p&gt;SOD package with 3.70 mm span with body size 2.70 X 1.55 X 1.35 mm&lt;/p&gt;</description>
<wire x1="1.425" y1="0.85" x2="-2.5991" y2="0.85" width="0.12" layer="21"/>
<wire x1="-2.5991" y1="0.85" x2="-2.5991" y2="-0.85" width="0.12" layer="21"/>
<wire x1="-2.5991" y1="-0.85" x2="1.425" y2="-0.85" width="0.12" layer="21"/>
<wire x1="1.425" y1="-0.85" x2="-1.425" y2="-0.85" width="0.12" layer="51"/>
<wire x1="-1.425" y1="-0.85" x2="-1.425" y2="0.85" width="0.12" layer="51"/>
<wire x1="-1.425" y1="0.85" x2="1.425" y2="0.85" width="0.12" layer="51"/>
<wire x1="1.425" y1="0.85" x2="1.425" y2="-0.85" width="0.12" layer="51"/>
<smd name="1" x="-1.7215" y="0" dx="1.1272" dy="0.7839" layer="1"/>
<smd name="2" x="1.7215" y="0" dx="1.1272" dy="0.7839" layer="1"/>
<text x="0" y="1.485" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-1.485" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="SOD6126X290" urn="urn:adsk.eagle:footprint:9427065/1">
<description>SOD, 6.10 mm span, 4.33 X 2.60 X 2.90 mm body
&lt;p&gt;SOD package with 6.10 mm span with body size 4.33 X 2.60 X 2.90 mm&lt;/p&gt;</description>
<wire x1="2.3" y1="1.475" x2="-3.9179" y2="1.475" width="0.12" layer="21"/>
<wire x1="-3.9179" y1="1.475" x2="-3.9179" y2="-1.475" width="0.12" layer="21"/>
<wire x1="-3.9179" y1="-1.475" x2="2.3" y2="-1.475" width="0.12" layer="21"/>
<wire x1="2.3" y1="-1.475" x2="-2.3" y2="-1.475" width="0.12" layer="51"/>
<wire x1="-2.3" y1="-1.475" x2="-2.3" y2="1.475" width="0.12" layer="51"/>
<wire x1="-2.3" y1="1.475" x2="2.3" y2="1.475" width="0.12" layer="51"/>
<wire x1="2.3" y1="1.475" x2="2.3" y2="-1.475" width="0.12" layer="51"/>
<smd name="1" x="-2.7048" y="0" dx="1.7981" dy="1.7253" layer="1"/>
<smd name="2" x="2.7048" y="0" dx="1.7981" dy="1.7253" layer="1"/>
<text x="0" y="2.11" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-2.11" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="SOD6126X350" urn="urn:adsk.eagle:footprint:9933385/1">
<description>SOD, 6.10 mm span, 4.20 X 2.65 X 3.50 mm body
&lt;p&gt;SOD package with 6.10 mm span with body size 4.20 X 2.65 X 3.50 mm&lt;/p&gt;</description>
<wire x1="2.225" y1="1.65" x2="-3.9179" y2="1.65" width="0.12" layer="21"/>
<wire x1="-3.9179" y1="1.65" x2="-3.9179" y2="-1.65" width="0.12" layer="21"/>
<wire x1="-3.9179" y1="-1.65" x2="2.225" y2="-1.65" width="0.12" layer="21"/>
<wire x1="2.225" y1="-1.65" x2="-2.225" y2="-1.65" width="0.12" layer="51"/>
<wire x1="-2.225" y1="-1.65" x2="-2.225" y2="1.65" width="0.12" layer="51"/>
<wire x1="-2.225" y1="1.65" x2="2.225" y2="1.65" width="0.12" layer="51"/>
<wire x1="2.225" y1="1.65" x2="2.225" y2="-1.65" width="0.12" layer="51"/>
<smd name="1" x="-2.7048" y="0" dx="1.7981" dy="1.7689" layer="1"/>
<smd name="2" x="2.7048" y="0" dx="1.7981" dy="1.7689" layer="1"/>
<text x="0" y="2.285" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-2.285" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="SOD6236X265" urn="urn:adsk.eagle:footprint:9427053/1">
<description>SOD, 6.22 mm span, 4.33 X 3.63 X 2.65 mm body
&lt;p&gt;SOD package with 6.22 mm span with body size 4.33 X 3.63 X 2.65 mm&lt;/p&gt;</description>
<wire x1="2.3" y1="1.975" x2="-3.9196" y2="1.975" width="0.12" layer="21"/>
<wire x1="-3.9196" y1="1.975" x2="-3.9196" y2="-1.975" width="0.12" layer="21"/>
<wire x1="-3.9196" y1="-1.975" x2="2.3" y2="-1.975" width="0.12" layer="21"/>
<wire x1="2.3" y1="-1.975" x2="-2.3" y2="-1.975" width="0.12" layer="51"/>
<wire x1="-2.3" y1="-1.975" x2="-2.3" y2="1.975" width="0.12" layer="51"/>
<wire x1="-2.3" y1="1.975" x2="2.3" y2="1.975" width="0.12" layer="51"/>
<wire x1="2.3" y1="1.975" x2="2.3" y2="-1.975" width="0.12" layer="51"/>
<smd name="1" x="-2.7561" y="0" dx="1.699" dy="2.2839" layer="1"/>
<smd name="2" x="2.7561" y="0" dx="1.699" dy="2.2839" layer="1"/>
<text x="0" y="2.61" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-2.61" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="SOD9959X265" urn="urn:adsk.eagle:footprint:9427066/1">
<description>SOD, 9.93 mm span, 6.88 X 5.90 X 2.65 mm body
&lt;p&gt;SOD package with 9.93 mm span with body size 6.88 X 5.90 X 2.65 mm&lt;/p&gt;</description>
<wire x1="3.575" y1="3.125" x2="-5.7696" y2="3.125" width="0.12" layer="21"/>
<wire x1="-5.7696" y1="3.125" x2="-5.7696" y2="-3.125" width="0.12" layer="21"/>
<wire x1="-5.7696" y1="-3.125" x2="3.575" y2="-3.125" width="0.12" layer="21"/>
<wire x1="3.575" y1="-3.125" x2="-3.575" y2="-3.125" width="0.12" layer="51"/>
<wire x1="-3.575" y1="-3.125" x2="-3.575" y2="3.125" width="0.12" layer="51"/>
<wire x1="-3.575" y1="3.125" x2="3.575" y2="3.125" width="0.12" layer="51"/>
<wire x1="3.575" y1="3.125" x2="3.575" y2="-3.125" width="0.12" layer="51"/>
<smd name="1" x="-4.5203" y="0" dx="1.8706" dy="3.2802" layer="1"/>
<smd name="2" x="4.5203" y="0" dx="1.8706" dy="3.2802" layer="1"/>
<text x="0" y="3.76" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-3.76" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="SODFL2513X70" urn="urn:adsk.eagle:footprint:9427167/1">
<description>SODFL, 2.50 mm span, 1.90 X 1.30 X 0.70 mm body
&lt;p&gt;SODFL package with 2.50 mm span with body size 1.90 X 1.30 X 0.70 mm&lt;/p&gt;</description>
<wire x1="1" y1="0.7009" x2="-1.8717" y2="0.7009" width="0.12" layer="21"/>
<wire x1="-1.8717" y1="0.7009" x2="-1.8717" y2="-0.7009" width="0.12" layer="21"/>
<wire x1="-1.8717" y1="-0.7009" x2="1" y2="-0.7009" width="0.12" layer="21"/>
<wire x1="1" y1="-0.7" x2="-1" y2="-0.7" width="0.12" layer="51"/>
<wire x1="-1" y1="-0.7" x2="-1" y2="0.7" width="0.12" layer="51"/>
<wire x1="-1" y1="0.7" x2="1" y2="0.7" width="0.12" layer="51"/>
<wire x1="1" y1="0.7" x2="1" y2="-0.7" width="0.12" layer="51"/>
<smd name="1" x="-1.065" y="0" dx="0.9854" dy="0.7739" layer="1"/>
<smd name="2" x="1.065" y="0" dx="0.9854" dy="0.7739" layer="1"/>
<text x="0" y="1.3359" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-1.3359" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="SODFL2513X75" urn="urn:adsk.eagle:footprint:9427168/1">
<description>SODFL, 2.50 mm span, 2.20 X 1.30 X 0.75 mm body
&lt;p&gt;SODFL package with 2.50 mm span with body size 2.20 X 1.30 X 0.75 mm&lt;/p&gt;</description>
<wire x1="1.15" y1="0.7009" x2="-1.8717" y2="0.7009" width="0.12" layer="21"/>
<wire x1="-1.8717" y1="0.7009" x2="-1.8717" y2="-0.7009" width="0.12" layer="21"/>
<wire x1="-1.8717" y1="-0.7009" x2="1.15" y2="-0.7009" width="0.12" layer="21"/>
<wire x1="1.15" y1="-0.7" x2="-1.15" y2="-0.7" width="0.12" layer="51"/>
<wire x1="-1.15" y1="-0.7" x2="-1.15" y2="0.7" width="0.12" layer="51"/>
<wire x1="-1.15" y1="0.7" x2="1.15" y2="0.7" width="0.12" layer="51"/>
<wire x1="1.15" y1="0.7" x2="1.15" y2="-0.7" width="0.12" layer="51"/>
<smd name="1" x="-0.7394" y="0" dx="1.6364" dy="1.003" layer="1"/>
<smd name="2" x="0.7394" y="0" dx="1.0027" dy="0.7739" layer="1"/>
<text x="0" y="1.3359" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-1.3359" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="SODFL3718X115" urn="urn:adsk.eagle:footprint:9427170/1">
<description>SODFL, 3.70 mm span, 2.80 X 1.80 X 1.15 mm body
&lt;p&gt;SODFL package with 3.70 mm span with body size 2.80 X 1.80 X 1.15 mm&lt;/p&gt;</description>
<wire x1="1.45" y1="0.9946" x2="-2.4717" y2="0.9946" width="0.12" layer="21"/>
<wire x1="-2.4717" y1="0.9946" x2="-2.4717" y2="-0.9946" width="0.12" layer="21"/>
<wire x1="-2.4717" y1="-0.9946" x2="1.45" y2="-0.9946" width="0.12" layer="21"/>
<wire x1="1.45" y1="-0.95" x2="-1.45" y2="-0.95" width="0.12" layer="51"/>
<wire x1="-1.45" y1="-0.95" x2="-1.45" y2="0.95" width="0.12" layer="51"/>
<wire x1="-1.45" y1="0.95" x2="1.45" y2="0.95" width="0.12" layer="51"/>
<wire x1="1.45" y1="0.95" x2="1.45" y2="-0.95" width="0.12" layer="51"/>
<smd name="1" x="-1.6004" y="0" dx="1.1146" dy="1.3612" layer="1"/>
<smd name="2" x="1.6004" y="0" dx="1.1146" dy="1.3612" layer="1"/>
<text x="0" y="1.6296" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-1.6296" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="SODFL3718X140" urn="urn:adsk.eagle:footprint:9427171/1">
<description>SODFL, 3.70 mm span, 2.80 X 1.80 X 1.40 mm body
&lt;p&gt;SODFL package with 3.70 mm span with body size 2.80 X 1.80 X 1.40 mm&lt;/p&gt;</description>
<wire x1="1.45" y1="0.9946" x2="-2.4717" y2="0.9946" width="0.12" layer="21"/>
<wire x1="-2.4717" y1="0.9946" x2="-2.4717" y2="-0.9946" width="0.12" layer="21"/>
<wire x1="-2.4717" y1="-0.9946" x2="1.45" y2="-0.9946" width="0.12" layer="21"/>
<wire x1="1.45" y1="-0.95" x2="-1.45" y2="-0.95" width="0.12" layer="51"/>
<wire x1="-1.45" y1="-0.95" x2="-1.45" y2="0.95" width="0.12" layer="51"/>
<wire x1="-1.45" y1="0.95" x2="1.45" y2="0.95" width="0.12" layer="51"/>
<wire x1="1.45" y1="0.95" x2="1.45" y2="-0.95" width="0.12" layer="51"/>
<smd name="1" x="-1.5233" y="0" dx="1.2688" dy="1.3612" layer="1"/>
<smd name="2" x="1.5233" y="0" dx="1.2688" dy="1.3612" layer="1"/>
<text x="0" y="1.6296" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-1.6296" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="SODFL5336X110" urn="urn:adsk.eagle:footprint:9427173/1">
<description>SODFL, 5.35 mm span, 4.33 X 3.63 X 1.10 mm body
&lt;p&gt;SODFL package with 5.35 mm span with body size 4.33 X 3.63 X 1.10 mm&lt;/p&gt;</description>
<wire x1="2.3" y1="1.975" x2="-3.3202" y2="1.975" width="0.12" layer="21"/>
<wire x1="-3.3202" y1="1.975" x2="-3.3202" y2="-1.975" width="0.12" layer="21"/>
<wire x1="-3.3202" y1="-1.975" x2="2.3" y2="-1.975" width="0.12" layer="21"/>
<wire x1="2.3" y1="-1.975" x2="-2.3" y2="-1.975" width="0.12" layer="51"/>
<wire x1="-2.3" y1="-1.975" x2="-2.3" y2="1.975" width="0.12" layer="51"/>
<wire x1="-2.3" y1="1.975" x2="2.3" y2="1.975" width="0.12" layer="51"/>
<wire x1="2.3" y1="1.975" x2="2.3" y2="-1.975" width="0.12" layer="51"/>
<smd name="1" x="-2.1302" y="0" dx="1.752" dy="2.2239" layer="1"/>
<smd name="2" x="2.1302" y="0" dx="1.752" dy="2.2239" layer="1"/>
<text x="0" y="2.61" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-2.61" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="SODFL7959X110" urn="urn:adsk.eagle:footprint:9427174/1">
<description>SODFL, 7.95 mm span, 6.88 X 5.90 X 1.10 mm body
&lt;p&gt;SODFL package with 7.95 mm span with body size 6.88 X 5.90 X 1.10 mm&lt;/p&gt;</description>
<wire x1="3.575" y1="3.125" x2="-4.5967" y2="3.125" width="0.12" layer="21"/>
<wire x1="-4.5967" y1="3.125" x2="-4.5967" y2="-3.125" width="0.12" layer="21"/>
<wire x1="-4.5967" y1="-3.125" x2="3.575" y2="-3.125" width="0.12" layer="21"/>
<wire x1="3.575" y1="-3.125" x2="-3.575" y2="-3.125" width="0.12" layer="51"/>
<wire x1="-3.575" y1="-3.125" x2="-3.575" y2="3.125" width="0.12" layer="51"/>
<wire x1="-3.575" y1="3.125" x2="3.575" y2="3.125" width="0.12" layer="51"/>
<wire x1="3.575" y1="3.125" x2="3.575" y2="-3.125" width="0.12" layer="51"/>
<smd name="1" x="-3.4233" y="0" dx="1.7188" dy="3.2202" layer="1"/>
<smd name="2" x="3.4233" y="0" dx="1.7188" dy="3.2202" layer="1"/>
<text x="0" y="3.76" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-3.76" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="SODFL5226X110" urn="urn:adsk.eagle:footprint:9427175/1">
<description>SODFL, 5.20 mm span, 4.28 X 2.60 X 1.10 mm body
&lt;p&gt;SODFL package with 5.20 mm span with body size 4.28 X 2.60 X 1.10 mm&lt;/p&gt;</description>
<wire x1="2.3" y1="1.475" x2="-3.3179" y2="1.475" width="0.12" layer="21"/>
<wire x1="-3.3179" y1="1.475" x2="-3.3179" y2="-1.475" width="0.12" layer="21"/>
<wire x1="-3.3179" y1="-1.475" x2="2.3" y2="-1.475" width="0.12" layer="21"/>
<wire x1="2.3" y1="-1.475" x2="-2.3" y2="-1.475" width="0.12" layer="51"/>
<wire x1="-2.3" y1="-1.475" x2="-2.3" y2="1.475" width="0.12" layer="51"/>
<wire x1="-2.3" y1="1.475" x2="2.3" y2="1.475" width="0.12" layer="51"/>
<wire x1="2.3" y1="1.475" x2="2.3" y2="-1.475" width="0.12" layer="51"/>
<smd name="1" x="-2.0722" y="0" dx="1.8634" dy="1.6653" layer="1"/>
<smd name="2" x="2.0722" y="0" dx="1.8634" dy="1.6653" layer="1"/>
<text x="0" y="2.11" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-2.11" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="SODFL4725X110" urn="urn:adsk.eagle:footprint:9427177/1">
<description>SODFL, 4.70 mm span, 3.80 X 2.50 X 1.10 mm body
&lt;p&gt;SODFL package with 4.70 mm span with body size 3.80 X 2.50 X 1.10 mm&lt;/p&gt;</description>
<wire x1="2" y1="1.35" x2="-3.0192" y2="1.35" width="0.12" layer="21"/>
<wire x1="-3.0192" y1="1.35" x2="-3.0192" y2="-1.35" width="0.12" layer="21"/>
<wire x1="-3.0192" y1="-1.35" x2="2" y2="-1.35" width="0.12" layer="21"/>
<wire x1="2" y1="-1.35" x2="-2" y2="-1.35" width="0.12" layer="51"/>
<wire x1="-2" y1="-1.35" x2="-2" y2="1.35" width="0.12" layer="51"/>
<wire x1="-2" y1="1.35" x2="2" y2="1.35" width="0.12" layer="51"/>
<wire x1="2" y1="1.35" x2="2" y2="-1.35" width="0.12" layer="51"/>
<smd name="1" x="-2.11" y="0" dx="1.1904" dy="2.0153" layer="1"/>
<smd name="2" x="2.11" y="0" dx="1.1904" dy="2.0153" layer="1"/>
<text x="0" y="1.985" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-1.985" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="SODFL1608X70" urn="urn:adsk.eagle:footprint:16378177/3">
<description>SODFL, 1.60 mm span, 1.20 X 0.80 X 0.70 mm body
&lt;p&gt;SODFL package with 1.60 mm span with body size 1.20 X 0.80 X 0.70 mm&lt;/p&gt;</description>
<wire x1="0.65" y1="0.514" x2="-1.3786" y2="0.514" width="0.12" layer="21"/>
<wire x1="-1.3786" y1="0.514" x2="-1.3786" y2="-0.514" width="0.12" layer="21"/>
<wire x1="-1.3786" y1="-0.514" x2="0.65" y2="-0.514" width="0.12" layer="21"/>
<wire x1="0.65" y1="-0.45" x2="-0.65" y2="-0.45" width="0.12" layer="51"/>
<wire x1="-0.65" y1="-0.45" x2="-0.65" y2="0.45" width="0.12" layer="51"/>
<wire x1="-0.65" y1="0.45" x2="0.65" y2="0.45" width="0.12" layer="51"/>
<wire x1="0.65" y1="0.45" x2="0.65" y2="-0.45" width="0.12" layer="51"/>
<smd name="1" x="-0.7956" y="0" dx="0.538" dy="0.4" layer="1"/>
<smd name="2" x="0.7956" y="0" dx="0.538" dy="0.4" layer="1"/>
<text x="0" y="1.149" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-1.149" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="DIOM5226X290N" urn="urn:adsk.eagle:footprint:16378179/3">
<description>Molded Body, 5.20 X 2.60 X 2.90 mm body
&lt;p&gt;Molded Body package with body size 5.20 X 2.60 X 2.90 mm&lt;/p&gt;</description>
<wire x1="2.8" y1="1.475" x2="-3.6179" y2="1.475" width="0.12" layer="21"/>
<wire x1="-3.6179" y1="1.475" x2="-3.6179" y2="-1.475" width="0.12" layer="21"/>
<wire x1="-3.6179" y1="-1.475" x2="2.8" y2="-1.475" width="0.12" layer="21"/>
<wire x1="2.8" y1="-1.475" x2="-2.8" y2="-1.475" width="0.12" layer="51"/>
<wire x1="-2.8" y1="-1.475" x2="-2.8" y2="1.475" width="0.12" layer="51"/>
<wire x1="-2.8" y1="1.475" x2="2.8" y2="1.475" width="0.12" layer="51"/>
<wire x1="2.8" y1="1.475" x2="2.8" y2="-1.475" width="0.12" layer="51"/>
<smd name="1" x="-2.1079" y="0" dx="2.392" dy="1.5653" layer="1"/>
<smd name="2" x="2.1079" y="0" dx="2.392" dy="1.5653" layer="1"/>
<text x="0" y="2.11" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-2.11" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="DIOM5336X265N" urn="urn:adsk.eagle:footprint:16378175/3">
<description>Molded Body, 5.35 X 3.63 X 2.65 mm body
&lt;p&gt;Molded Body package with body size 5.35 X 3.63 X 2.65 mm&lt;/p&gt;</description>
<wire x1="2.8" y1="1.975" x2="-3.6202" y2="1.975" width="0.12" layer="21"/>
<wire x1="-3.6202" y1="1.975" x2="-3.6202" y2="-1.975" width="0.12" layer="21"/>
<wire x1="-3.6202" y1="-1.975" x2="2.8" y2="-1.975" width="0.12" layer="21"/>
<wire x1="2.8" y1="-1.975" x2="-2.8" y2="-1.975" width="0.12" layer="51"/>
<wire x1="-2.8" y1="-1.975" x2="-2.8" y2="1.975" width="0.12" layer="51"/>
<wire x1="-2.8" y1="1.975" x2="2.8" y2="1.975" width="0.12" layer="51"/>
<wire x1="2.8" y1="1.975" x2="2.8" y2="-1.975" width="0.12" layer="51"/>
<smd name="1" x="-2.1641" y="0" dx="2.2841" dy="2.1239" layer="1"/>
<smd name="2" x="2.1641" y="0" dx="2.2841" dy="2.1239" layer="1"/>
<text x="0" y="2.61" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-2.61" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="DIOM7959X625N" urn="urn:adsk.eagle:footprint:16378174/3">
<description>Molded Body, 7.95 X 5.90 X 6.25 mm body
&lt;p&gt;Molded Body package with body size 7.95 X 5.90 X 6.25 mm&lt;/p&gt;</description>
<wire x1="4.075" y1="3.125" x2="-4.8967" y2="3.125" width="0.12" layer="21"/>
<wire x1="-4.8967" y1="3.125" x2="-4.8967" y2="-3.125" width="0.12" layer="21"/>
<wire x1="-4.8967" y1="-3.125" x2="4.075" y2="-3.125" width="0.12" layer="21"/>
<wire x1="4.075" y1="-3.125" x2="-4.075" y2="-3.125" width="0.12" layer="51"/>
<wire x1="-4.075" y1="-3.125" x2="-4.075" y2="3.125" width="0.12" layer="51"/>
<wire x1="-4.075" y1="3.125" x2="4.075" y2="3.125" width="0.12" layer="51"/>
<wire x1="4.075" y1="3.125" x2="4.075" y2="-3.125" width="0.12" layer="51"/>
<smd name="1" x="-3.4567" y="0" dx="2.2518" dy="3.1202" layer="1"/>
<smd name="2" x="3.4567" y="0" dx="2.2518" dy="3.1202" layer="1"/>
<text x="0" y="3.76" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-3.76" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
</packages>
<packages3d>
<package3d name="DIOMELF3516L" urn="urn:adsk.eagle:package:16378190/4" type="model">
<description>MELF, 3.50 mm length, 1.65 mm diameter
&lt;p&gt;MELF Diode package with 3.50 mm length and 1.65 mm diameter&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="DIOMELF3516"/>
</packageinstances>
</package3d>
<package3d name="DIOMELF5024" urn="urn:adsk.eagle:package:16378191/3" type="model">
<description>MELF, 5.00 mm length, 2.49 mm diameter
&lt;p&gt;MELF Diode package with 5.00 mm length and 2.49 mm diameter&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="DIOMELF5024"/>
</packageinstances>
</package3d>
<package3d name="SOD3715X135" urn="urn:adsk.eagle:package:9427058/2" type="model">
<description>SOD, 3.70 mm span, 2.70 X 1.55 X 1.35 mm body
&lt;p&gt;SOD package with 3.70 mm span with body size 2.70 X 1.55 X 1.35 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="SOD3715X135"/>
</packageinstances>
</package3d>
<package3d name="SOD6126X290" urn="urn:adsk.eagle:package:9427057/2" type="model">
<description>SOD, 6.10 mm span, 4.33 X 2.60 X 2.90 mm body
&lt;p&gt;SOD package with 6.10 mm span with body size 4.33 X 2.60 X 2.90 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="SOD6126X290"/>
</packageinstances>
</package3d>
<package3d name="SOD6126X350" urn="urn:adsk.eagle:package:9932483/2" type="model">
<description>SOD, 6.10 mm span, 4.20 X 2.65 X 3.50 mm body
&lt;p&gt;SOD package with 6.10 mm span with body size 4.20 X 2.65 X 3.50 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="SOD6126X350"/>
</packageinstances>
</package3d>
<package3d name="SOD6236X265" urn="urn:adsk.eagle:package:9427046/2" type="model">
<description>SOD, 6.22 mm span, 4.33 X 3.63 X 2.65 mm body
&lt;p&gt;SOD package with 6.22 mm span with body size 4.33 X 3.63 X 2.65 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="SOD6236X265"/>
</packageinstances>
</package3d>
<package3d name="SOD9959X265" urn="urn:adsk.eagle:package:9427056/2" type="model">
<description>SOD, 9.93 mm span, 6.88 X 5.90 X 2.65 mm body
&lt;p&gt;SOD package with 9.93 mm span with body size 6.88 X 5.90 X 2.65 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="SOD9959X265"/>
</packageinstances>
</package3d>
<package3d name="SODFL2513X70" urn="urn:adsk.eagle:package:9427155/2" type="model">
<description>SODFL, 2.50 mm span, 1.90 X 1.30 X 0.70 mm body
&lt;p&gt;SODFL package with 2.50 mm span with body size 1.90 X 1.30 X 0.70 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="SODFL2513X70"/>
</packageinstances>
</package3d>
<package3d name="SODFL2513X75" urn="urn:adsk.eagle:package:9427154/2" type="model">
<description>SODFL, 2.50 mm span, 2.20 X 1.30 X 0.75 mm body
&lt;p&gt;SODFL package with 2.50 mm span with body size 2.20 X 1.30 X 0.75 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="SODFL2513X75"/>
</packageinstances>
</package3d>
<package3d name="SODFL3718X115" urn="urn:adsk.eagle:package:9427153/2" type="model">
<description>SODFL, 3.70 mm span, 2.80 X 1.80 X 1.15 mm body
&lt;p&gt;SODFL package with 3.70 mm span with body size 2.80 X 1.80 X 1.15 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="SODFL3718X115"/>
</packageinstances>
</package3d>
<package3d name="SODFL3718X140" urn="urn:adsk.eagle:package:9427152/2" type="model">
<description>SODFL, 3.70 mm span, 2.80 X 1.80 X 1.40 mm body
&lt;p&gt;SODFL package with 3.70 mm span with body size 2.80 X 1.80 X 1.40 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="SODFL3718X140"/>
</packageinstances>
</package3d>
<package3d name="SODFL5336X110" urn="urn:adsk.eagle:package:9427151/2" type="model">
<description>SODFL, 5.35 mm span, 4.33 X 3.63 X 1.10 mm body
&lt;p&gt;SODFL package with 5.35 mm span with body size 4.33 X 3.63 X 1.10 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="SODFL5336X110"/>
</packageinstances>
</package3d>
<package3d name="SODFL7959X110" urn="urn:adsk.eagle:package:9427150/2" type="model">
<description>SODFL, 7.95 mm span, 6.88 X 5.90 X 1.10 mm body
&lt;p&gt;SODFL package with 7.95 mm span with body size 6.88 X 5.90 X 1.10 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="SODFL7959X110"/>
</packageinstances>
</package3d>
<package3d name="SODFL5226X110" urn="urn:adsk.eagle:package:9427148/2" type="model">
<description>SODFL, 5.20 mm span, 4.28 X 2.60 X 1.10 mm body
&lt;p&gt;SODFL package with 5.20 mm span with body size 4.28 X 2.60 X 1.10 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="SODFL5226X110"/>
</packageinstances>
</package3d>
<package3d name="SODFL4725X110" urn="urn:adsk.eagle:package:9427149/2" type="model">
<description>SODFL, 4.70 mm span, 3.80 X 2.50 X 1.10 mm body
&lt;p&gt;SODFL package with 4.70 mm span with body size 3.80 X 2.50 X 1.10 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="SODFL4725X110"/>
</packageinstances>
</package3d>
<package3d name="SODFL1608X70" urn="urn:adsk.eagle:package:16378187/3" type="model">
<description>SODFL, 1.60 mm span, 1.20 X 0.80 X 0.70 mm body
&lt;p&gt;SODFL package with 1.60 mm span with body size 1.20 X 0.80 X 0.70 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="SODFL1608X70"/>
</packageinstances>
</package3d>
<package3d name="DIOM5226X290N" urn="urn:adsk.eagle:package:16378188/3" type="model">
<description>Molded Body, 5.20 X 2.60 X 2.90 mm body
&lt;p&gt;Molded Body package with body size 5.20 X 2.60 X 2.90 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="DIOM5226X290N"/>
</packageinstances>
</package3d>
<package3d name="DIOM5336X265N" urn="urn:adsk.eagle:package:16378189/3" type="model">
<description>Molded Body, 5.35 X 3.63 X 2.65 mm body
&lt;p&gt;Molded Body package with body size 5.35 X 3.63 X 2.65 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="DIOM5336X265N"/>
</packageinstances>
</package3d>
<package3d name="DIOM7959X625N" urn="urn:adsk.eagle:package:16378186/3" type="model">
<description>Molded Body, 7.95 X 5.90 X 6.25 mm body
&lt;p&gt;Molded Body package with body size 7.95 X 5.90 X 6.25 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="DIOM7959X625N"/>
</packageinstances>
</package3d>
</packages3d>
<symbols>
<symbol name="ZD" urn="urn:adsk.eagle:symbol:16378172/2">
<wire x1="-1.27" y1="-1.27" x2="1.27" y2="0" width="0.254" layer="94"/>
<wire x1="1.27" y1="0" x2="-1.27" y2="1.27" width="0.254" layer="94"/>
<wire x1="1.27" y1="1.27" x2="1.27" y2="0" width="0.254" layer="94"/>
<wire x1="-1.27" y1="1.27" x2="-1.27" y2="0" width="0.254" layer="94"/>
<wire x1="-1.27" y1="0" x2="-1.27" y2="-1.27" width="0.254" layer="94"/>
<wire x1="1.27" y1="0" x2="1.27" y2="-1.27" width="0.254" layer="94"/>
<wire x1="1.27" y1="-1.27" x2="0.635" y2="-1.27" width="0.254" layer="94"/>
<wire x1="-1.27" y1="0" x2="-2.54" y2="0" width="0.254" layer="94"/>
<wire x1="1.27" y1="0" x2="2.54" y2="0" width="0.254" layer="94"/>
<text x="0" y="3.175" size="1.778" layer="95" align="center">&gt;NAME</text>
<text x="0" y="-3.429" size="1.778" layer="96" align="center">&gt;VALUE</text>
<pin name="A" x="-2.54" y="0" visible="off" length="point" direction="pas"/>
<pin name="C" x="2.54" y="0" visible="off" length="point" direction="pas" rot="R180"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="ZENER" urn="urn:adsk.eagle:component:16494886/6" prefix="D">
<description>&lt;B&gt;Zener Diode - Generic</description>
<gates>
<gate name="G$1" symbol="ZD" x="0" y="0"/>
</gates>
<devices>
<device name="DO-213AA(SOD-80)" package="DIOMELF3516">
<connects>
<connect gate="G$1" pin="A" pad="2"/>
<connect gate="G$1" pin="C" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:16378190/4"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Diode" constant="no"/>
<attribute name="DESCRIPTION" value="" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Zener" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
<attribute name="VALUE" value="ZENER" constant="no"/>
<attribute name="ZENER_VOLTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="DO-213AB(5025-METRIC)" package="DIOMELF5024">
<connects>
<connect gate="G$1" pin="A" pad="2"/>
<connect gate="G$1" pin="C" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:16378191/3"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Diode" constant="no"/>
<attribute name="DESCRIPTION" value="" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Zener" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
<attribute name="VALUE" value="ZENER" constant="no"/>
<attribute name="ZENER_VOLTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="DO-215-AD" package="SOD3715X135">
<connects>
<connect gate="G$1" pin="A" pad="2"/>
<connect gate="G$1" pin="C" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:9427058/2"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Diode" constant="no"/>
<attribute name="DESCRIPTION" value="" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Zener" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
<attribute name="VALUE" value="ZENER" constant="no"/>
<attribute name="ZENER_VOLTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="DO-215-AC" package="SOD6126X290">
<connects>
<connect gate="G$1" pin="A" pad="2"/>
<connect gate="G$1" pin="C" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:9427057/2"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Diode" constant="no"/>
<attribute name="DESCRIPTION" value="" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Zener" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
<attribute name="VALUE" value="ZENER" constant="no"/>
<attribute name="ZENER_VOLTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="DO-215-BA" package="SOD6126X350">
<connects>
<connect gate="G$1" pin="A" pad="2"/>
<connect gate="G$1" pin="C" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:9932483/2"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Diode" constant="no"/>
<attribute name="DESCRIPTION" value="" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Zener" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
<attribute name="VALUE" value="ZENER" constant="no"/>
<attribute name="ZENER_VOLTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="DO-215-AA" package="SOD6236X265">
<connects>
<connect gate="G$1" pin="A" pad="2"/>
<connect gate="G$1" pin="C" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:9427046/2"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Diode" constant="no"/>
<attribute name="DESCRIPTION" value="" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Zener" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
<attribute name="VALUE" value="ZENER" constant="no"/>
<attribute name="ZENER_VOLTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="DO-215-AB" package="SOD9959X265">
<connects>
<connect gate="G$1" pin="A" pad="2"/>
<connect gate="G$1" pin="C" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:9427056/2"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Diode" constant="no"/>
<attribute name="DESCRIPTION" value="" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Zener" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
<attribute name="VALUE" value="ZENER" constant="no"/>
<attribute name="ZENER_VOLTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="DO-219-AC(SOD323F)" package="SODFL2513X70">
<connects>
<connect gate="G$1" pin="A" pad="2"/>
<connect gate="G$1" pin="C" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:9427155/2"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Diode" constant="no"/>
<attribute name="DESCRIPTION" value="" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Zener" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
<attribute name="VALUE" value="ZENER" constant="no"/>
<attribute name="ZENER_VOLTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="DO-219-AD" package="SODFL2513X75">
<connects>
<connect gate="G$1" pin="A" pad="2"/>
<connect gate="G$1" pin="C" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:9427154/2"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Diode" constant="no"/>
<attribute name="DESCRIPTION" value="" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Zener" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
<attribute name="VALUE" value="ZENER" constant="no"/>
<attribute name="ZENER_VOLTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="DO-219-AB(SOD123F)" package="SODFL3718X115">
<connects>
<connect gate="G$1" pin="A" pad="2"/>
<connect gate="G$1" pin="C" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:9427153/2"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Diode" constant="no"/>
<attribute name="DESCRIPTION" value="" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Zener" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
<attribute name="VALUE" value="ZENER" constant="no"/>
<attribute name="ZENER_VOLTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="DO-219-AA" package="SODFL3718X140">
<connects>
<connect gate="G$1" pin="A" pad="2"/>
<connect gate="G$1" pin="C" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:9427152/2"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Diode" constant="no"/>
<attribute name="DESCRIPTION" value="" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Zener" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
<attribute name="VALUE" value="ZENER" constant="no"/>
<attribute name="ZENER_VOLTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="DO-221-AA" package="SODFL5336X110">
<connects>
<connect gate="G$1" pin="A" pad="2"/>
<connect gate="G$1" pin="C" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:9427151/2"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Diode" constant="no"/>
<attribute name="DESCRIPTION" value="" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Zener" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
<attribute name="VALUE" value="ZENER" constant="no"/>
<attribute name="ZENER_VOLTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="DO-221-AB" package="SODFL7959X110">
<connects>
<connect gate="G$1" pin="A" pad="2"/>
<connect gate="G$1" pin="C" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:9427150/2"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Diode" constant="no"/>
<attribute name="DESCRIPTION" value="" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Zener" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
<attribute name="VALUE" value="ZENER" constant="no"/>
<attribute name="ZENER_VOLTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="DO-221-AC" package="SODFL5226X110">
<connects>
<connect gate="G$1" pin="A" pad="2"/>
<connect gate="G$1" pin="C" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:9427148/2"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Diode" constant="no"/>
<attribute name="DESCRIPTION" value="" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Zener" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
<attribute name="VALUE" value="ZENER" constant="no"/>
<attribute name="ZENER_VOLTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="DO-221-AD" package="SODFL4725X110">
<connects>
<connect gate="G$1" pin="A" pad="2"/>
<connect gate="G$1" pin="C" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:9427149/2"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Diode" constant="no"/>
<attribute name="DESCRIPTION" value="" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Zener" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
<attribute name="VALUE" value="ZENER" constant="no"/>
<attribute name="ZENER_VOLTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="SODFL(1608-METRIC)" package="SODFL1608X70">
<connects>
<connect gate="G$1" pin="A" pad="2"/>
<connect gate="G$1" pin="C" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:16378187/3"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Diode" constant="no"/>
<attribute name="DESCRIPTION" value="" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Zener" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
<attribute name="VALUE" value="ZENER" constant="no"/>
<attribute name="ZENER_VOLTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="DO-214AC(SMA)" package="DIOM5226X290N">
<connects>
<connect gate="G$1" pin="A" pad="2"/>
<connect gate="G$1" pin="C" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:16378188/3"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="CATEGORY" value="Diode" constant="no"/>
<attribute name="DESCRIPTION" value="" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Zener" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
<attribute name="VALUE" value="ZENER" constant="no"/>
<attribute name="ZENER_VOLTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="DO-214AA(SMB)" package="DIOM5336X265N">
<connects>
<connect gate="G$1" pin="A" pad="2"/>
<connect gate="G$1" pin="C" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:16378189/3"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="CATEGORY" value="Diode" constant="no"/>
<attribute name="DESCRIPTION" value="" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Zener" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
<attribute name="VALUE" value="ZENER" constant="no"/>
<attribute name="ZENER_VOLTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="DO-214AB(SMC)" package="DIOM7959X625N">
<connects>
<connect gate="G$1" pin="A" pad="2"/>
<connect gate="G$1" pin="C" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:16378186/3"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="CATEGORY" value="Diode" constant="no"/>
<attribute name="DESCRIPTION" value="" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Zener" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
<attribute name="VALUE" value="ZENER" constant="no"/>
<attribute name="ZENER_VOLTAGE" value="" constant="no"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="Resistor">
<description>&lt;B&gt;Resistors, Potentiometers, TrimPot</description>
<packages>
<package name="RESC1005X40" urn="urn:adsk.eagle:footprint:16378540/5">
<description>Chip, 1.05 X 0.54 X 0.40 mm body
&lt;p&gt;Chip package with body size 1.05 X 0.54 X 0.40 mm&lt;/p&gt;</description>
<wire x1="0.55" y1="0.636" x2="-0.55" y2="0.636" width="0.127" layer="21"/>
<wire x1="0.55" y1="-0.636" x2="-0.55" y2="-0.636" width="0.127" layer="21"/>
<wire x1="0.55" y1="-0.3" x2="-0.55" y2="-0.3" width="0.12" layer="51"/>
<wire x1="-0.55" y1="-0.3" x2="-0.55" y2="0.3" width="0.12" layer="51"/>
<wire x1="-0.55" y1="0.3" x2="0.55" y2="0.3" width="0.12" layer="51"/>
<wire x1="0.55" y1="0.3" x2="0.55" y2="-0.3" width="0.12" layer="51"/>
<smd name="1" x="-0.5075" y="0" dx="0.5351" dy="0.644" layer="1"/>
<smd name="2" x="0.5075" y="0" dx="0.5351" dy="0.644" layer="1"/>
<text x="0" y="1.271" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-1.271" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="RESC1608X60" urn="urn:adsk.eagle:footprint:16378537/5">
<description>Chip, 1.60 X 0.82 X 0.60 mm body
&lt;p&gt;Chip package with body size 1.60 X 0.82 X 0.60 mm&lt;/p&gt;</description>
<wire x1="0.85" y1="0.8009" x2="-0.85" y2="0.8009" width="0.127" layer="21"/>
<wire x1="0.85" y1="-0.8009" x2="-0.85" y2="-0.8009" width="0.127" layer="21"/>
<wire x1="0.85" y1="-0.475" x2="-0.85" y2="-0.475" width="0.12" layer="51"/>
<wire x1="-0.85" y1="-0.475" x2="-0.85" y2="0.475" width="0.12" layer="51"/>
<wire x1="-0.85" y1="0.475" x2="0.85" y2="0.475" width="0.12" layer="51"/>
<wire x1="0.85" y1="0.475" x2="0.85" y2="-0.475" width="0.12" layer="51"/>
<smd name="1" x="-0.8152" y="0" dx="0.7987" dy="0.9739" layer="1"/>
<smd name="2" x="0.8152" y="0" dx="0.7987" dy="0.9739" layer="1"/>
<text x="0" y="1.4359" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-1.4359" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="RESC2012X65" urn="urn:adsk.eagle:footprint:16378532/5">
<description>Chip, 2.00 X 1.25 X 0.65 mm body
&lt;p&gt;Chip package with body size 2.00 X 1.25 X 0.65 mm&lt;/p&gt;</description>
<wire x1="1.075" y1="1.0241" x2="-1.075" y2="1.0241" width="0.127" layer="21"/>
<wire x1="1.075" y1="-1.0241" x2="-1.075" y2="-1.0241" width="0.127" layer="21"/>
<wire x1="1.075" y1="-0.7" x2="-1.075" y2="-0.7" width="0.12" layer="51"/>
<wire x1="-1.075" y1="-0.7" x2="-1.075" y2="0.7" width="0.12" layer="51"/>
<wire x1="-1.075" y1="0.7" x2="1.075" y2="0.7" width="0.12" layer="51"/>
<wire x1="1.075" y1="0.7" x2="1.075" y2="-0.7" width="0.12" layer="51"/>
<smd name="1" x="-0.9195" y="0" dx="1.0312" dy="1.4202" layer="1"/>
<smd name="2" x="0.9195" y="0" dx="1.0312" dy="1.4202" layer="1"/>
<text x="0" y="1.6591" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-1.6591" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="RESC3216X70" urn="urn:adsk.eagle:footprint:16378539/5">
<description>Chip, 3.20 X 1.60 X 0.70 mm body
&lt;p&gt;Chip package with body size 3.20 X 1.60 X 0.70 mm&lt;/p&gt;</description>
<wire x1="1.7" y1="1.2217" x2="-1.7" y2="1.2217" width="0.127" layer="21"/>
<wire x1="1.7" y1="-1.2217" x2="-1.7" y2="-1.2217" width="0.127" layer="21"/>
<wire x1="1.7" y1="-0.9" x2="-1.7" y2="-0.9" width="0.12" layer="51"/>
<wire x1="-1.7" y1="-0.9" x2="-1.7" y2="0.9" width="0.12" layer="51"/>
<wire x1="-1.7" y1="0.9" x2="1.7" y2="0.9" width="0.12" layer="51"/>
<wire x1="1.7" y1="0.9" x2="1.7" y2="-0.9" width="0.12" layer="51"/>
<smd name="1" x="-1.4754" y="0" dx="1.1646" dy="1.8153" layer="1"/>
<smd name="2" x="1.4754" y="0" dx="1.1646" dy="1.8153" layer="1"/>
<text x="0" y="1.8567" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-1.8567" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="RESC3224X71" urn="urn:adsk.eagle:footprint:16378536/5">
<description>Chip, 3.20 X 2.49 X 0.71 mm body
&lt;p&gt;Chip package with body size 3.20 X 2.49 X 0.71 mm&lt;/p&gt;</description>
<wire x1="1.675" y1="1.6441" x2="-1.675" y2="1.6441" width="0.127" layer="21"/>
<wire x1="1.675" y1="-1.6441" x2="-1.675" y2="-1.6441" width="0.127" layer="21"/>
<wire x1="1.675" y1="-1.32" x2="-1.675" y2="-1.32" width="0.12" layer="51"/>
<wire x1="-1.675" y1="-1.32" x2="-1.675" y2="1.32" width="0.12" layer="51"/>
<wire x1="-1.675" y1="1.32" x2="1.675" y2="1.32" width="0.12" layer="51"/>
<wire x1="1.675" y1="1.32" x2="1.675" y2="-1.32" width="0.12" layer="51"/>
<smd name="1" x="-1.4695" y="0" dx="1.1312" dy="2.6602" layer="1"/>
<smd name="2" x="1.4695" y="0" dx="1.1312" dy="2.6602" layer="1"/>
<text x="0" y="2.2791" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-2.2791" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="RESC5025X71" urn="urn:adsk.eagle:footprint:16378538/5">
<description>Chip, 5.00 X 2.50 X 0.71 mm body
&lt;p&gt;Chip package with body size 5.00 X 2.50 X 0.71 mm&lt;/p&gt;</description>
<wire x1="2.575" y1="1.6491" x2="-2.575" y2="1.6491" width="0.127" layer="21"/>
<wire x1="2.575" y1="-1.6491" x2="-2.575" y2="-1.6491" width="0.127" layer="21"/>
<wire x1="2.575" y1="-1.325" x2="-2.575" y2="-1.325" width="0.12" layer="51"/>
<wire x1="-2.575" y1="-1.325" x2="-2.575" y2="1.325" width="0.12" layer="51"/>
<wire x1="-2.575" y1="1.325" x2="2.575" y2="1.325" width="0.12" layer="51"/>
<wire x1="2.575" y1="1.325" x2="2.575" y2="-1.325" width="0.12" layer="51"/>
<smd name="1" x="-2.3195" y="0" dx="1.2312" dy="2.6702" layer="1"/>
<smd name="2" x="2.3195" y="0" dx="1.2312" dy="2.6702" layer="1"/>
<text x="0" y="2.2841" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-2.2841" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="RESC6332X71" urn="urn:adsk.eagle:footprint:16378533/5">
<description>Chip, 6.30 X 3.20 X 0.71 mm body
&lt;p&gt;Chip package with body size 6.30 X 3.20 X 0.71 mm&lt;/p&gt;</description>
<wire x1="3.225" y1="1.9991" x2="-3.225" y2="1.9991" width="0.127" layer="21"/>
<wire x1="3.225" y1="-1.9991" x2="-3.225" y2="-1.9991" width="0.127" layer="21"/>
<wire x1="3.225" y1="-1.675" x2="-3.225" y2="-1.675" width="0.12" layer="51"/>
<wire x1="-3.225" y1="-1.675" x2="-3.225" y2="1.675" width="0.12" layer="51"/>
<wire x1="-3.225" y1="1.675" x2="3.225" y2="1.675" width="0.12" layer="51"/>
<wire x1="3.225" y1="1.675" x2="3.225" y2="-1.675" width="0.12" layer="51"/>
<smd name="1" x="-2.9695" y="0" dx="1.2312" dy="3.3702" layer="1"/>
<smd name="2" x="2.9695" y="0" dx="1.2312" dy="3.3702" layer="1"/>
<text x="0" y="2.6341" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-2.6341" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="RESAD1176W63L850D250B" urn="urn:adsk.eagle:footprint:16378542/5">
<description>AXIAL Resistor, 11.76 mm pitch, 8.5 mm body length, 2.5 mm body diameter
&lt;p&gt;AXIAL Resistor package with 11.76 mm pitch, 0.63 mm lead diameter, 8.5 mm body length and 2.5 mm body diameter&lt;/p&gt;</description>
<wire x1="-4.25" y1="1.25" x2="-4.25" y2="-1.25" width="0.127" layer="21"/>
<wire x1="-4.25" y1="-1.25" x2="4.25" y2="-1.25" width="0.127" layer="21"/>
<wire x1="4.25" y1="-1.25" x2="4.25" y2="1.25" width="0.127" layer="21"/>
<wire x1="4.25" y1="1.25" x2="-4.25" y2="1.25" width="0.127" layer="21"/>
<wire x1="-4.25" y1="0" x2="-4.911" y2="0" width="0.127" layer="21"/>
<wire x1="4.25" y1="0" x2="4.911" y2="0" width="0.127" layer="21"/>
<wire x1="4.25" y1="-1.25" x2="-4.25" y2="-1.25" width="0.12" layer="51"/>
<wire x1="-4.25" y1="-1.25" x2="-4.25" y2="1.25" width="0.12" layer="51"/>
<wire x1="-4.25" y1="1.25" x2="4.25" y2="1.25" width="0.12" layer="51"/>
<wire x1="4.25" y1="1.25" x2="4.25" y2="-1.25" width="0.12" layer="51"/>
<pad name="1" x="-5.88" y="0" drill="0.83" diameter="1.43"/>
<pad name="2" x="5.88" y="0" drill="0.83" diameter="1.43"/>
<text x="0" y="1.885" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-1.885" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="RESMELF3515" urn="urn:adsk.eagle:footprint:16378534/5">
<description>MELF, 3.50 mm length, 1.52 mm diameter
&lt;p&gt;MELF Resistor package with 3.50 mm length and 1.52 mm diameter&lt;/p&gt;</description>
<wire x1="1.105" y1="1.1825" x2="-1.105" y2="1.1825" width="0.127" layer="21"/>
<wire x1="-1.105" y1="-1.1825" x2="1.105" y2="-1.1825" width="0.127" layer="21"/>
<wire x1="1.85" y1="-0.8" x2="-1.85" y2="-0.8" width="0.12" layer="51"/>
<wire x1="-1.85" y1="-0.8" x2="-1.85" y2="0.8" width="0.12" layer="51"/>
<wire x1="-1.85" y1="0.8" x2="1.85" y2="0.8" width="0.12" layer="51"/>
<wire x1="1.85" y1="0.8" x2="1.85" y2="-0.8" width="0.12" layer="51"/>
<smd name="1" x="-1.6813" y="0" dx="1.1527" dy="1.7371" layer="1"/>
<smd name="2" x="1.6813" y="0" dx="1.1527" dy="1.7371" layer="1"/>
<text x="0" y="1.8175" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-1.8175" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="RESMELF2014" urn="urn:adsk.eagle:footprint:16378535/5">
<description>MELF, 2.00 mm length, 1.40 mm diameter
&lt;p&gt;MELF Resistor package with 2.00 mm length and 1.40 mm diameter&lt;/p&gt;</description>
<wire x1="0.5189" y1="1.114" x2="-0.5189" y2="1.114" width="0.127" layer="21"/>
<wire x1="-0.5189" y1="-1.114" x2="0.5189" y2="-1.114" width="0.127" layer="21"/>
<wire x1="1.05" y1="-0.725" x2="-1.05" y2="-0.725" width="0.12" layer="51"/>
<wire x1="-1.05" y1="-0.725" x2="-1.05" y2="0.725" width="0.12" layer="51"/>
<wire x1="-1.05" y1="0.725" x2="1.05" y2="0.725" width="0.12" layer="51"/>
<wire x1="1.05" y1="0.725" x2="1.05" y2="-0.725" width="0.12" layer="51"/>
<smd name="1" x="-0.9918" y="0" dx="0.9456" dy="1.6" layer="1"/>
<smd name="2" x="0.9918" y="0" dx="0.9456" dy="1.6" layer="1"/>
<text x="0" y="1.749" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-1.749" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="RESMELF5924" urn="urn:adsk.eagle:footprint:16378541/5">
<description>MELF, 5.90 mm length, 2.45 mm diameter
&lt;p&gt;MELF Resistor package with 5.90 mm length and 2.45 mm diameter&lt;/p&gt;</description>
<wire x1="2.1315" y1="1.639" x2="-2.1315" y2="1.639" width="0.127" layer="21"/>
<wire x1="-2.1315" y1="-1.639" x2="2.1315" y2="-1.639" width="0.127" layer="21"/>
<wire x1="3.05" y1="-1.25" x2="-3.05" y2="-1.25" width="0.12" layer="51"/>
<wire x1="-3.05" y1="-1.25" x2="-3.05" y2="1.25" width="0.12" layer="51"/>
<wire x1="-3.05" y1="1.25" x2="3.05" y2="1.25" width="0.12" layer="51"/>
<wire x1="3.05" y1="1.25" x2="3.05" y2="-1.25" width="0.12" layer="51"/>
<smd name="1" x="-2.7946" y="0" dx="1.3261" dy="2.65" layer="1"/>
<smd name="2" x="2.7946" y="0" dx="1.3261" dy="2.65" layer="1"/>
<text x="0" y="2.274" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-2.274" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="RESMELF3218" urn="urn:adsk.eagle:footprint:16378531/5">
<description>MELF, 3.20 mm length, 1.80 mm diameter
&lt;p&gt;MELF Resistor package with 3.20 mm length and 1.80 mm diameter&lt;/p&gt;</description>
<wire x1="0.8815" y1="1.314" x2="-0.8815" y2="1.314" width="0.127" layer="21"/>
<wire x1="-0.8815" y1="-1.314" x2="0.8815" y2="-1.314" width="0.127" layer="21"/>
<wire x1="1.7" y1="-0.925" x2="-1.7" y2="-0.925" width="0.12" layer="51"/>
<wire x1="-1.7" y1="-0.925" x2="-1.7" y2="0.925" width="0.12" layer="51"/>
<wire x1="-1.7" y1="0.925" x2="1.7" y2="0.925" width="0.12" layer="51"/>
<wire x1="1.7" y1="0.925" x2="1.7" y2="-0.925" width="0.12" layer="51"/>
<smd name="1" x="-1.4946" y="0" dx="1.2261" dy="2" layer="1"/>
<smd name="2" x="1.4946" y="0" dx="1.2261" dy="2" layer="1"/>
<text x="0" y="1.949" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-1.949" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="RESAD724W46L381D178B" urn="urn:adsk.eagle:footprint:16378530/5">
<description>Axial Resistor, 7.24 mm pitch, 3.81 mm body length, 1.78 mm body diameter
&lt;p&gt;Axial Resistor package with 7.24 mm pitch (lead spacing), 0.46 mm lead diameter, 3.81 mm body length and 1.78 mm body diameter&lt;/p&gt;</description>
<wire x1="-2.16" y1="1.015" x2="-2.16" y2="-1.015" width="0.127" layer="21"/>
<wire x1="-2.16" y1="-1.015" x2="2.16" y2="-1.015" width="0.127" layer="21"/>
<wire x1="2.16" y1="-1.015" x2="2.16" y2="1.015" width="0.127" layer="21"/>
<wire x1="2.16" y1="1.015" x2="-2.16" y2="1.015" width="0.127" layer="21"/>
<wire x1="-2.16" y1="0" x2="-2.736" y2="0" width="0.127" layer="21"/>
<wire x1="2.16" y1="0" x2="2.736" y2="0" width="0.127" layer="21"/>
<wire x1="2.16" y1="-1.015" x2="-2.16" y2="-1.015" width="0.12" layer="51"/>
<wire x1="-2.16" y1="-1.015" x2="-2.16" y2="1.015" width="0.12" layer="51"/>
<wire x1="-2.16" y1="1.015" x2="2.16" y2="1.015" width="0.12" layer="51"/>
<wire x1="2.16" y1="1.015" x2="2.16" y2="-1.015" width="0.12" layer="51"/>
<pad name="1" x="-3.62" y="0" drill="0.66" diameter="1.26"/>
<pad name="2" x="3.62" y="0" drill="0.66" diameter="1.26"/>
<text x="0" y="1.65" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-1.65" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="PV36P" urn="urn:adsk.eagle:footprint:24935629/3">
<description>PV36P</description>
<circle x="-3" y="0" radius="0.25" width="0" layer="21"/>
<wire x1="7.42" y1="-4.925" x2="-2.36" y2="-4.925" width="0.12" layer="21"/>
<wire x1="-2.36" y1="-4.925" x2="-2.36" y2="5.355" width="0.12" layer="21"/>
<wire x1="-2.36" y1="5.355" x2="7.42" y2="5.355" width="0.12" layer="21"/>
<wire x1="7.42" y1="5.355" x2="7.42" y2="-4.925" width="0.12" layer="21"/>
<pad name="1" x="0" y="0" drill="1" diameter="1.7"/>
<pad name="2" x="2.54" y="-2.54" drill="1" diameter="1.7"/>
<pad name="3" x="5.08" y="0" drill="1" diameter="1.7"/>
<text x="2.53" y="5.969" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="2.53" y="-5.365" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="PV36W" urn="urn:adsk.eagle:footprint:24935628/3">
<description>PV36W</description>
<circle x="-3" y="0" radius="0.25" width="0" layer="21"/>
<wire x1="7.43" y1="-2.485" x2="-2.35" y2="-2.485" width="0.12" layer="21"/>
<wire x1="-2.35" y1="-2.485" x2="-2.35" y2="2.475" width="0.12" layer="21"/>
<wire x1="-2.35" y1="2.475" x2="7.43" y2="2.475" width="0.12" layer="21"/>
<wire x1="7.43" y1="2.475" x2="7.43" y2="-2.485" width="0.12" layer="21"/>
<pad name="3" x="5.08" y="0" drill="1" diameter="1.7"/>
<pad name="2" x="2.54" y="0" drill="1" diameter="1.7"/>
<pad name="1" x="0" y="0" drill="1" diameter="1.7"/>
<text x="2.54" y="3" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="2.54" y="-3.115" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="PV36X" urn="urn:adsk.eagle:footprint:24935627/3">
<description>PV36X</description>
<circle x="-3" y="0" radius="0.25" width="0" layer="21"/>
<wire x1="7.43" y1="-2.485" x2="-2.35" y2="-2.485" width="0.12" layer="21"/>
<wire x1="-2.35" y1="-2.485" x2="-2.35" y2="2.475" width="0.12" layer="21"/>
<wire x1="7.43" y1="2.475" x2="7.43" y2="-2.485" width="0.12" layer="21"/>
<wire x1="-2.35" y1="2.475" x2="7.43" y2="2.475" width="0.12" layer="21"/>
<pad name="3" x="5.08" y="0" drill="1" diameter="1.7"/>
<pad name="2" x="2.54" y="0" drill="1" diameter="1.7"/>
<pad name="1" x="0" y="0" drill="1" diameter="1.7"/>
<text x="2.54" y="3" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="2.54" y="-3.115" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="PV36Y" urn="urn:adsk.eagle:footprint:24935626/3">
<description>PV36Y</description>
<circle x="-3" y="0" radius="0.25" width="0" layer="21"/>
<wire x1="7.43" y1="-1.215" x2="-2.35" y2="-1.215" width="0.12" layer="21"/>
<wire x1="-2.35" y1="-1.215" x2="-2.35" y2="3.745" width="0.12" layer="21"/>
<wire x1="-2.35" y1="3.745" x2="7.43" y2="3.745" width="0.12" layer="21"/>
<wire x1="7.43" y1="3.745" x2="7.43" y2="-1.215" width="0.12" layer="21"/>
<pad name="1" x="0" y="0" drill="1" diameter="1.5637"/>
<pad name="2" x="2.54" y="2.54" drill="1" diameter="1.5637"/>
<pad name="3" x="5.08" y="0" drill="1" diameter="1.5637"/>
<text x="2.54" y="4.5" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="2.54" y="-1.845" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="PV36Z" urn="urn:adsk.eagle:footprint:24935625/3">
<description>PV36Z</description>
<circle x="-3" y="0" radius="0.25" width="0" layer="21"/>
<wire x1="7.43" y1="-1.215" x2="-2.35" y2="-1.215" width="0.12" layer="21"/>
<wire x1="-2.35" y1="-1.215" x2="-2.35" y2="3.745" width="0.12" layer="21"/>
<wire x1="-2.35" y1="3.745" x2="7.43" y2="3.745" width="0.12" layer="21"/>
<wire x1="7.43" y1="3.745" x2="7.43" y2="-1.215" width="0.12" layer="21"/>
<pad name="1" x="0" y="0" drill="1" diameter="1.5637"/>
<pad name="2" x="2.54" y="2.54" drill="1" diameter="1.5637"/>
<pad name="3" x="5.08" y="0" drill="1" diameter="1.5637"/>
<text x="2.54" y="4.5" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="2.54" y="-1.845" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
</packages>
<packages3d>
<package3d name="RESC1005X40" urn="urn:adsk.eagle:package:16378568/5" type="model">
<description>Chip, 1.05 X 0.54 X 0.40 mm body
&lt;p&gt;Chip package with body size 1.05 X 0.54 X 0.40 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="RESC1005X40"/>
</packageinstances>
</package3d>
<package3d name="RESC1608X60" urn="urn:adsk.eagle:package:16378565/5" type="model">
<description>Chip, 1.60 X 0.82 X 0.60 mm body
&lt;p&gt;Chip package with body size 1.60 X 0.82 X 0.60 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="RESC1608X60"/>
</packageinstances>
</package3d>
<package3d name="RESC2012X65" urn="urn:adsk.eagle:package:16378559/5" type="model">
<description>Chip, 2.00 X 1.25 X 0.65 mm body
&lt;p&gt;Chip package with body size 2.00 X 1.25 X 0.65 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="RESC2012X65"/>
</packageinstances>
</package3d>
<package3d name="RESC3216X70" urn="urn:adsk.eagle:package:16378566/5" type="model">
<description>Chip, 3.20 X 1.60 X 0.70 mm body
&lt;p&gt;Chip package with body size 3.20 X 1.60 X 0.70 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="RESC3216X70"/>
</packageinstances>
</package3d>
<package3d name="RESC3224X71" urn="urn:adsk.eagle:package:16378563/6" type="model">
<description>Chip, 3.20 X 2.49 X 0.71 mm body
&lt;p&gt;Chip package with body size 3.20 X 2.49 X 0.71 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="RESC3224X71"/>
</packageinstances>
</package3d>
<package3d name="RESC5025X71" urn="urn:adsk.eagle:package:16378564/5" type="model">
<description>Chip, 5.00 X 2.50 X 0.71 mm body
&lt;p&gt;Chip package with body size 5.00 X 2.50 X 0.71 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="RESC5025X71"/>
</packageinstances>
</package3d>
<package3d name="RESC6332X71L" urn="urn:adsk.eagle:package:16378557/6" type="model">
<description>Chip, 6.30 X 3.20 X 0.71 mm body
&lt;p&gt;Chip package with body size 6.30 X 3.20 X 0.71 mm&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="RESC6332X71"/>
</packageinstances>
</package3d>
<package3d name="RESAD1176W63L850D250B" urn="urn:adsk.eagle:package:16378560/5" type="model">
<description>AXIAL Resistor, 11.76 mm pitch, 8.5 mm body length, 2.5 mm body diameter
&lt;p&gt;AXIAL Resistor package with 11.76 mm pitch, 0.63 mm lead diameter, 8.5 mm body length and 2.5 mm body diameter&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="RESAD1176W63L850D250B"/>
</packageinstances>
</package3d>
<package3d name="RESMELF3515" urn="urn:adsk.eagle:package:16378562/5" type="model">
<description>MELF, 3.50 mm length, 1.52 mm diameter
&lt;p&gt;MELF Resistor package with 3.50 mm length and 1.52 mm diameter&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="RESMELF3515"/>
</packageinstances>
</package3d>
<package3d name="RESMELF2014" urn="urn:adsk.eagle:package:16378558/5" type="model">
<description>MELF, 2.00 mm length, 1.40 mm diameter
&lt;p&gt;MELF Resistor package with 2.00 mm length and 1.40 mm diameter&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="RESMELF2014"/>
</packageinstances>
</package3d>
<package3d name="RESMELF5924" urn="urn:adsk.eagle:package:16378567/6" type="model">
<description>MELF, 5.90 mm length, 2.45 mm diameter
&lt;p&gt;MELF Resistor package with 5.90 mm length and 2.45 mm diameter&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="RESMELF5924"/>
</packageinstances>
</package3d>
<package3d name="RESMELF3218" urn="urn:adsk.eagle:package:16378556/5" type="model">
<description>MELF, 3.20 mm length, 1.80 mm diameter
&lt;p&gt;MELF Resistor package with 3.20 mm length and 1.80 mm diameter&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="RESMELF3218"/>
</packageinstances>
</package3d>
<package3d name="RESAD724W46L381D178B" urn="urn:adsk.eagle:package:16378561/5" type="model">
<description>Axial Resistor, 7.24 mm pitch, 3.81 mm body length, 1.78 mm body diameter
&lt;p&gt;Axial Resistor package with 7.24 mm pitch (lead spacing), 0.46 mm lead diameter, 3.81 mm body length and 1.78 mm body diameter&lt;/p&gt;</description>
<packageinstances>
<packageinstance name="RESAD724W46L381D178B"/>
</packageinstances>
</package3d>
<package3d name="PV36P" urn="urn:adsk.eagle:package:24935635/4" type="model">
<description>PV36P</description>
<packageinstances>
<packageinstance name="PV36P"/>
</packageinstances>
</package3d>
<package3d name="PV36W" urn="urn:adsk.eagle:package:24935634/4" type="model">
<description>PV36W</description>
<packageinstances>
<packageinstance name="PV36W"/>
</packageinstances>
</package3d>
<package3d name="PV36X" urn="urn:adsk.eagle:package:24935633/4" type="model">
<description>PV36X</description>
<packageinstances>
<packageinstance name="PV36X"/>
</packageinstances>
</package3d>
<package3d name="PV36Y" urn="urn:adsk.eagle:package:24935632/4" type="model">
<description>PV36Y</description>
<packageinstances>
<packageinstance name="PV36Y"/>
</packageinstances>
</package3d>
<package3d name="PV36Z" urn="urn:adsk.eagle:package:24935631/4" type="model">
<description>PV36Z</description>
<packageinstances>
<packageinstance name="PV36Z"/>
</packageinstances>
</package3d>
</packages3d>
<symbols>
<symbol name="R" urn="urn:adsk.eagle:symbol:16378529/3">
<description>RESISTOR</description>
<wire x1="-2.54" y1="-0.889" x2="2.54" y2="-0.889" width="0.254" layer="94"/>
<wire x1="2.54" y1="0.889" x2="-2.54" y2="0.889" width="0.254" layer="94"/>
<wire x1="2.54" y1="-0.889" x2="2.54" y2="0.889" width="0.254" layer="94"/>
<wire x1="-2.54" y1="-0.889" x2="-2.54" y2="0.889" width="0.254" layer="94"/>
<pin name="1" x="-5.08" y="0" visible="off" length="short" direction="pas" swaplevel="1"/>
<pin name="2" x="5.08" y="0" visible="off" length="short" direction="pas" swaplevel="1" rot="R180"/>
<text x="0" y="2.54" size="1.778" layer="95" align="center">&gt;NAME</text>
<text x="0" y="-5.08" size="1.778" layer="95" align="center">&gt;SPICEMODEL</text>
<text x="0" y="-2.54" size="1.778" layer="96" align="center">&gt;VALUE</text>
<text x="0" y="-7.62" size="1.778" layer="95" align="center">&gt;SPICEEXTRA</text>
</symbol>
<symbol name="TRIM-POT" urn="urn:adsk.eagle:symbol:24935630/2">
<wire x1="-5.08" y1="1.27" x2="-5.08" y2="-1.27" width="0.4064" layer="94"/>
<wire x1="-5.08" y1="-1.27" x2="5.08" y2="-1.27" width="0.4064" layer="94"/>
<wire x1="5.08" y1="-1.27" x2="5.08" y2="1.27" width="0.4064" layer="94"/>
<wire x1="5.08" y1="1.27" x2="-5.08" y2="1.27" width="0.4064" layer="94"/>
<wire x1="-2.54" y1="2.54" x2="2.54" y2="2.54" width="0.4064" layer="94"/>
<pin name="P$1" x="-7.62" y="0" visible="pad" length="short" direction="pas"/>
<pin name="P$3" x="7.62" y="0" visible="pad" length="short" direction="pas" rot="R180"/>
<pin name="P$2" x="0" y="5.08" visible="pad" length="short" direction="pas" rot="R270"/>
<text x="1.27" y="3.81" size="1.778" layer="95">&gt;NAME</text>
<text x="1.27" y="-3.81" size="1.778" layer="96">&gt;VALUE</text>
</symbol>
</symbols>
<devicesets>
<deviceset name="R" urn="urn:adsk.eagle:component:16378570/10" prefix="R" uservalue="yes">
<description>&lt;b&gt;Resistor Fixed - Generic</description>
<gates>
<gate name="G$1" symbol="R" x="0" y="0"/>
</gates>
<devices>
<device name="CHIP-0402(1005-METRIC)" package="RESC1005X40">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:16378568/5"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Resistor" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="RATING" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Fixed" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TOLERANCE" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="CHIP-0603(1608-METRIC)" package="RESC1608X60">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:16378565/5"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Resistor" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="RATING" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Fixed" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TOLERANCE" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="CHIP-0805(2012-METRIC)" package="RESC2012X65">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:16378559/5"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Resistor" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="RATING" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Fixed" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TOLERANCE" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="CHIP-1206(3216-METRIC)" package="RESC3216X70">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:16378566/5"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Resistor" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="RATING" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Fixed" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TOLERANCE" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="CHIP-1210(3225-METRIC)" package="RESC3224X71">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:16378563/6"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Resistor" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="RATING" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Fixed" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TOLERANCE" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="CHIP-2010(5025-METRIC)" package="RESC5025X71">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:16378564/5"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Resistor" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="RATING" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Fixed" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TOLERANCE" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="CHIP-2512(6332-METRIC)" package="RESC6332X71">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:16378557/6"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Resistor" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="RATING" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Fixed" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TOLERANCE" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="AXIAL-11.7MM-PITCH" package="RESAD1176W63L850D250B">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:16378560/5"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Resistor" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="RATING" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Fixed" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TOLERANCE" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="MELF(3515-METRIC)" package="RESMELF3515">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:16378562/5"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Resistor" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="RATING" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Fixed" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TOLERANCE" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="MELF(2014-METRIC)" package="RESMELF2014">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:16378558/5"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Resistor" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="RATING" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Fixed" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TOLERANCE" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="MELF(5924-METRIC)" package="RESMELF5924">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:16378567/6"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Resistor" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="RATING" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Fixed" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TOLERANCE" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="MELF(3218-METRIC)" package="RESMELF3218">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:16378556/5"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Resistor" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="RATING" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Fixed" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TOLERANCE" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="AXIAL-7.2MM-PITCH" package="RESAD724W46L381D178B">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:16378561/5"/>
</package3dinstances>
<technologies>
<technology name="_">
<attribute name="CATEGORY" value="Resistor" constant="no"/>
<attribute name="MANUFACTURER" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OPERATING_TEMP" value="" constant="no"/>
<attribute name="PART_STATUS" value="" constant="no"/>
<attribute name="RATING" value="" constant="no"/>
<attribute name="ROHS_COMPLIANT" value="" constant="no"/>
<attribute name="SERIES" value="" constant="no"/>
<attribute name="SUB-CATEGORY" value="Fixed" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TOLERANCE" value="" constant="no"/>
<attribute name="TYPE" value="" constant="no"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="PV36" urn="urn:adsk.eagle:component:24935636/6" prefix="R" uservalue="yes">
<description>Rectangular Trimmer Potentiometers - PV36 Series
&lt;br&gt;&lt;br&gt;&lt;a href="https://www.bourns.com/docs/Product-Datasheets/pv36.pdf"&gt;Datasheet&lt;br&gt;</description>
<gates>
<gate name="G$1" symbol="TRIM-POT" x="0" y="0"/>
</gates>
<devices>
<device name="P" package="PV36P">
<connects>
<connect gate="G$1" pin="P$1" pad="1"/>
<connect gate="G$1" pin="P$2" pad="2"/>
<connect gate="G$1" pin="P$3" pad="3"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:24935635/4"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="CATEGORY" value="Resistor" constant="no"/>
<attribute name="DESCRIPTION" value="Lead Sealed Type Multiturn PV36 Series" constant="no"/>
<attribute name="MANUFACTURER" value="BOURNS" constant="no"/>
<attribute name="MPN" value="PV36P" constant="no"/>
<attribute name="OPERATING_TEMPERATURE" value=" -55 to +125 °C" constant="no"/>
<attribute name="PART_STATUS" value="Active" constant="no"/>
<attribute name="ROHS_COMPLIANCE" value="RoHS Compliant" constant="no"/>
<attribute name="SERIES" value="PV36" constant="no"/>
<attribute name="SUB-CATEGORY" value="Trimpot" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="Lead Sealed" constant="no"/>
</technology>
</technologies>
</device>
<device name="W" package="PV36W">
<connects>
<connect gate="G$1" pin="P$1" pad="1"/>
<connect gate="G$1" pin="P$2" pad="2"/>
<connect gate="G$1" pin="P$3" pad="3"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:24935634/4"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="CATEGORY" value="Resistor" constant="no"/>
<attribute name="DESCRIPTION" value="Lead Sealed Type Multiturn PV36 Series" constant="no"/>
<attribute name="MANUFACTURER" value="BOURNS" constant="no"/>
<attribute name="MPN" value="PV36W" constant="no"/>
<attribute name="OPERATING_TEMPERATURE" value=" -55 to +125 °C" constant="no"/>
<attribute name="PART_STATUS" value="Active" constant="no"/>
<attribute name="ROHS_COMPLIANCE" value="RoHS Compliant" constant="no"/>
<attribute name="SERIES" value="PV36" constant="no"/>
<attribute name="SUB-CATEGORY" value="Trimpot" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="Lead Sealed" constant="no"/>
</technology>
</technologies>
</device>
<device name="X" package="PV36X">
<connects>
<connect gate="G$1" pin="P$1" pad="1"/>
<connect gate="G$1" pin="P$2" pad="2"/>
<connect gate="G$1" pin="P$3" pad="3"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:24935633/4"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="CATEGORY" value="Resistor" constant="no"/>
<attribute name="DESCRIPTION" value="Lead Sealed Type Multiturn PV36 Series" constant="no"/>
<attribute name="MANUFACTURER" value="BOURNS" constant="no"/>
<attribute name="MPN" value="PV36X" constant="no"/>
<attribute name="OPERATING_TEMPERATURE" value=" -55 to +125 °C" constant="no"/>
<attribute name="PART_STATUS" value="Active" constant="no"/>
<attribute name="ROHS_COMPLIANCE" value="RoHS Compliant" constant="no"/>
<attribute name="SERIES" value="PV36" constant="no"/>
<attribute name="SUB-CATEGORY" value="Trimpot" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="Lead sealed" constant="no"/>
</technology>
</technologies>
</device>
<device name="Y" package="PV36Y">
<connects>
<connect gate="G$1" pin="P$1" pad="1"/>
<connect gate="G$1" pin="P$2" pad="2"/>
<connect gate="G$1" pin="P$3" pad="3"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:24935632/4"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="CATEGORY" value="Resistor" constant="no"/>
<attribute name="DESCRIPTION" value="Lead Sealed Type Multiturn PV36 Series" constant="no"/>
<attribute name="MANUFACTURER" value="BOURNS" constant="no"/>
<attribute name="MPN" value="PV36Y" constant="no"/>
<attribute name="OPERATING_TEMPERATURE" value="-55 to +125 °C" constant="no"/>
<attribute name="PART_STATUS" value="Active" constant="no"/>
<attribute name="ROHS_COMPLIANCE" value="ROHS Compliant" constant="no"/>
<attribute name="SERIES" value="PV36" constant="no"/>
<attribute name="SUB-CATEGORY" value="Trimpot" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="Lead Sealed" constant="no"/>
</technology>
</technologies>
</device>
<device name="Z" package="PV36Z">
<connects>
<connect gate="G$1" pin="P$1" pad="1"/>
<connect gate="G$1" pin="P$2" pad="2"/>
<connect gate="G$1" pin="P$3" pad="3"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:24935631/4"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="CATEGORY" value="Resistor" constant="no"/>
<attribute name="DESCRIPTION" value="Lead Sealed Type Multiturn PV36 Series" constant="no"/>
<attribute name="MANUFACTURER" value="BOURNS" constant="no"/>
<attribute name="MPN" value="PV36Z" constant="no"/>
<attribute name="OPERATING_TEMPERATURE" value=" -55 to +125 °C" constant="no"/>
<attribute name="PART_STATUS" value="Active" constant="no"/>
<attribute name="ROHS_COMPLIANCE" value="RoHS Compliant" constant="no"/>
<attribute name="SERIES" value="PV36" constant="no"/>
<attribute name="SUB-CATEGORY" value="Trimpot" constant="no"/>
<attribute name="THERMALLOSS" value="" constant="no"/>
<attribute name="TYPE" value="Lead Sealed" constant="no"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="Power_Symbols">
<description>&lt;B&gt;Supply &amp; Ground symbols</description>
<packages>
</packages>
<symbols>
<symbol name="AGND" urn="urn:adsk.eagle:symbol:18498250/2">
<description>Analog Ground (AGND) Arrow</description>
<wire x1="-1.27" y1="0" x2="1.27" y2="0" width="0.254" layer="94"/>
<wire x1="1.27" y1="0" x2="0" y2="-1.27" width="0.254" layer="94"/>
<wire x1="0" y1="-1.27" x2="-1.27" y2="0" width="0.254" layer="94"/>
<text x="-0.127" y="-3.683" size="1.778" layer="96" align="bottom-center">&gt;VALUE</text>
<pin name="AGND" x="0" y="2.54" visible="off" length="short" direction="sup" rot="R270"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="AGND" urn="urn:adsk.eagle:component:16502427/7" prefix="SUPPLY" uservalue="yes">
<description>&lt;b&gt;SUPPLY SYMBOL&lt;/b&gt; - Analog Ground (AGND) Arrow</description>
<gates>
<gate name="G$1" symbol="AGND" x="0" y="0"/>
</gates>
<devices>
<device name="">
<technologies>
<technology name="">
<attribute name="CATEGORY" value="Supply" constant="no"/>
<attribute name="VALUE" value="AGND" constant="no"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
</libraries>
<attributes>
</attributes>
<variantdefs>
</variantdefs>
<classes>
<class number="0" name="default" width="0" drill="0">
</class>
</classes>
<parts>
<part name="U2" library="RpiPico" deviceset="RASPBERRY_PICO" device="TH"/>
<part name="DRIBBLERS" library="Terminal Blocks" library_urn="urn:adsk.eagle:library:11886498" deviceset="691311400106" device="" package3d_urn="urn:adsk.eagle:package:11836875/2"/>
<part name="ARMS" library="Terminal Blocks" library_urn="urn:adsk.eagle:library:11886498" deviceset="691311400106" device="" package3d_urn="urn:adsk.eagle:package:11836875/2"/>
<part name="D1" library="Diode" deviceset="ZENER" device="DO-214AB(SMC)" package3d_urn="urn:adsk.eagle:package:16378186/3" value="ZENER"/>
<part name="R1" library="Resistor" deviceset="R" device="AXIAL-7.2MM-PITCH" package3d_urn="urn:adsk.eagle:package:16378561/5" technology="_"/>
<part name="R2" library="Resistor" deviceset="R" device="AXIAL-7.2MM-PITCH" package3d_urn="urn:adsk.eagle:package:16378561/5" technology="_"/>
<part name="SUPPLY1" library="Power_Symbols" deviceset="AGND" device="" value="AGND"/>
<part name="SUPPLY2" library="Power_Symbols" deviceset="AGND" device="" value="AGND"/>
<part name="TOFS" library="Terminal Blocks" library_urn="urn:adsk.eagle:library:11886498" deviceset="691311400106" device="" package3d_urn="urn:adsk.eagle:package:11836875/2"/>
<part name="SUPPLY3" library="Power_Symbols" deviceset="AGND" device="" value="AGND"/>
<part name="I2C" library="Connector" deviceset="2828XX-2" device="282834-2" package3d_urn="urn:adsk.eagle:package:24957623/1"/>
<part name="DRIBBLERS_PWM" library="Connector" deviceset="2828XX-2" device="282834-2" package3d_urn="urn:adsk.eagle:package:24957623/1"/>
<part name="ARMS_PWM" library="Connector" deviceset="2828XX-2" device="282834-2" package3d_urn="urn:adsk.eagle:package:24957623/1"/>
<part name="SUPPLY4" library="Power_Symbols" deviceset="AGND" device="" value="AGND"/>
<part name="SUPPLY5" library="Power_Symbols" deviceset="AGND" device="" value="AGND"/>
<part name="KICK" library="Connector" deviceset="2828XX-3" device="282837-3" package3d_urn="urn:adsk.eagle:package:24957620/1"/>
<part name="SUPPLY6" library="Power_Symbols" deviceset="AGND" device="" value="AGND"/>
<part name="SUPPLY7" library="Power_Symbols" deviceset="AGND" device="" value="AGND"/>
<part name="R3" library="Resistor" deviceset="PV36" device="Z" package3d_urn="urn:adsk.eagle:package:24935631/4"/>
</parts>
<sheets>
<sheet>
<plain>
</plain>
<instances>
<instance part="U2" gate="U$1" x="38.1" y="129.54" smashed="yes">
<attribute name="NAME" x="25.3845" y="168.9546" size="2.54388125" layer="95"/>
<attribute name="VALUE" x="25.3931" y="87.6086" size="2.54171875" layer="96"/>
</instance>
<instance part="DRIBBLERS" gate="G$1" x="-38.1" y="137.16" smashed="yes">
<attribute name="NAME" x="-55.88" y="137.16" size="1.778" layer="95"/>
</instance>
<instance part="ARMS" gate="G$1" x="-38.1" y="116.84" smashed="yes">
<attribute name="NAME" x="-50.8" y="116.84" size="1.778" layer="95"/>
</instance>
<instance part="D1" gate="G$1" x="99.06" y="93.98" smashed="yes" rot="R90">
<attribute name="NAME" x="95.885" y="93.98" size="1.778" layer="95" rot="R90" align="center"/>
<attribute name="VALUE" x="102.489" y="93.98" size="1.778" layer="96" rot="R90" align="center"/>
</instance>
<instance part="R1" gate="G$1" x="91.44" y="127" smashed="yes" rot="R90">
<attribute name="NAME" x="88.9" y="127" size="1.778" layer="95" rot="R90" align="center"/>
<attribute name="VALUE" x="93.98" y="127" size="1.778" layer="96" rot="R90" align="center"/>
</instance>
<instance part="R2" gate="G$1" x="91.44" y="93.98" smashed="yes" rot="R90">
<attribute name="NAME" x="88.9" y="93.98" size="1.778" layer="95" rot="R90" align="center"/>
<attribute name="VALUE" x="93.98" y="93.98" size="1.778" layer="96" rot="R90" align="center"/>
</instance>
<instance part="SUPPLY1" gate="G$1" x="91.44" y="83.82" smashed="yes">
<attribute name="VALUE" x="91.313" y="80.137" size="1.778" layer="96" align="bottom-center"/>
</instance>
<instance part="SUPPLY2" gate="G$1" x="99.06" y="83.82" smashed="yes">
<attribute name="VALUE" x="98.933" y="80.137" size="1.778" layer="96" align="bottom-center"/>
</instance>
<instance part="TOFS" gate="G$1" x="-22.86" y="154.94" smashed="yes">
<attribute name="NAME" x="-33.02" y="154.94" size="1.778" layer="95"/>
</instance>
<instance part="SUPPLY3" gate="G$1" x="-12.7" y="157.48" smashed="yes" rot="R90">
<attribute name="VALUE" x="-9.017" y="157.353" size="1.778" layer="96" rot="R90" align="bottom-center"/>
</instance>
<instance part="I2C" gate="G$1" x="68.58" y="119.38" smashed="yes">
<attribute name="NAME" x="68.58" y="127.254" size="1.778" layer="95" align="bottom-center"/>
</instance>
<instance part="DRIBBLERS_PWM" gate="G$1" x="-50.8" y="149.86" smashed="yes" rot="MR0">
<attribute name="NAME" x="-66.04" y="150.114" size="1.778" layer="95" rot="MR0" align="bottom-center"/>
</instance>
<instance part="ARMS_PWM" gate="G$1" x="-38.1" y="96.52" smashed="yes" rot="MR0">
<attribute name="NAME" x="-48.26" y="96.774" size="1.778" layer="95" rot="MR0" align="bottom-center"/>
</instance>
<instance part="SUPPLY4" gate="G$1" x="-43.18" y="149.86" smashed="yes" rot="R90">
<attribute name="VALUE" x="-39.497" y="149.733" size="1.778" layer="96" rot="R90" align="bottom-center"/>
</instance>
<instance part="SUPPLY5" gate="G$1" x="-30.48" y="96.52" smashed="yes" rot="R90">
<attribute name="VALUE" x="-26.797" y="96.393" size="1.778" layer="96" rot="R90" align="bottom-center"/>
</instance>
<instance part="KICK" gate="G$1" x="106.68" y="132.08" smashed="yes">
<attribute name="NAME" x="106.68" y="137.414" size="1.778" layer="95" align="bottom-center"/>
</instance>
<instance part="SUPPLY6" gate="G$1" x="58.42" y="93.98" smashed="yes" rot="R90">
<attribute name="VALUE" x="62.103" y="93.853" size="1.778" layer="96" rot="R90" align="bottom-center"/>
</instance>
<instance part="SUPPLY7" gate="G$1" x="99.06" y="129.54" smashed="yes" rot="MR90">
<attribute name="VALUE" x="95.377" y="129.413" size="1.778" layer="96" rot="MR90" align="bottom-center"/>
</instance>
<instance part="R3" gate="G$1" x="91.44" y="111.76" smashed="yes" rot="R90">
<attribute name="NAME" x="87.63" y="113.03" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="95.25" y="113.03" size="1.778" layer="96" rot="R90"/>
</instance>
</instances>
<busses>
</busses>
<nets>
<net name="KICK" class="0">
<segment>
<pinref part="U2" gate="U$1" pin="GP1"/>
<wire x1="-15.24" y1="152.4" x2="20.32" y2="152.4" width="0.1524" layer="91"/>
<pinref part="TOFS" gate="G$1" pin="4"/>
</segment>
</net>
<net name="N$2" class="0">
<segment>
<pinref part="U2" gate="U$1" pin="GP3"/>
<wire x1="20.32" y1="144.78" x2="10.16" y2="144.78" width="0.1524" layer="91"/>
<wire x1="-15.24" y1="147.32" x2="10.16" y2="147.32" width="0.1524" layer="91"/>
<wire x1="10.16" y1="147.32" x2="10.16" y2="144.78" width="0.1524" layer="91"/>
<pinref part="TOFS" gate="G$1" pin="6"/>
</segment>
</net>
<net name="N$3" class="0">
<segment>
<pinref part="U2" gate="U$1" pin="GP2"/>
<wire x1="20.32" y1="147.32" x2="12.7" y2="147.32" width="0.1524" layer="91"/>
<wire x1="-15.24" y1="149.86" x2="12.7" y2="149.86" width="0.1524" layer="91"/>
<wire x1="12.7" y1="149.86" x2="12.7" y2="147.32" width="0.1524" layer="91"/>
<pinref part="TOFS" gate="G$1" pin="5"/>
</segment>
</net>
<net name="TOF_SDA" class="0">
<segment>
<pinref part="U2" gate="U$1" pin="GP0"/>
<wire x1="-15.24" y1="154.94" x2="20.32" y2="154.94" width="0.1524" layer="91"/>
<pinref part="TOFS" gate="G$1" pin="3"/>
</segment>
</net>
<net name="N$1" class="0">
<segment>
<pinref part="DRIBBLERS" gate="G$1" pin="1"/>
<wire x1="-30.48" y1="142.24" x2="20.32" y2="142.24" width="0.1524" layer="91"/>
<pinref part="U2" gate="U$1" pin="GP4"/>
</segment>
</net>
<net name="N$4" class="0">
<segment>
<pinref part="DRIBBLERS" gate="G$1" pin="2"/>
<wire x1="-30.48" y1="139.7" x2="20.32" y2="139.7" width="0.1524" layer="91"/>
<pinref part="U2" gate="U$1" pin="GP5"/>
</segment>
</net>
<net name="N$5" class="0">
<segment>
<pinref part="DRIBBLERS" gate="G$1" pin="3"/>
<wire x1="-30.48" y1="137.16" x2="15.24" y2="137.16" width="0.1524" layer="91"/>
<wire x1="15.24" y1="137.16" x2="15.24" y2="134.62" width="0.1524" layer="91"/>
<wire x1="15.24" y1="134.62" x2="20.32" y2="134.62" width="0.1524" layer="91"/>
<pinref part="U2" gate="U$1" pin="GP6"/>
</segment>
</net>
<net name="N$6" class="0">
<segment>
<pinref part="DRIBBLERS" gate="G$1" pin="4"/>
<wire x1="-30.48" y1="134.62" x2="12.7" y2="134.62" width="0.1524" layer="91"/>
<wire x1="12.7" y1="134.62" x2="12.7" y2="132.08" width="0.1524" layer="91"/>
<wire x1="12.7" y1="132.08" x2="20.32" y2="132.08" width="0.1524" layer="91"/>
<pinref part="U2" gate="U$1" pin="GP7"/>
</segment>
</net>
<net name="N$7" class="0">
<segment>
<pinref part="DRIBBLERS" gate="G$1" pin="5"/>
<wire x1="-30.48" y1="132.08" x2="10.16" y2="132.08" width="0.1524" layer="91"/>
<wire x1="10.16" y1="132.08" x2="10.16" y2="129.54" width="0.1524" layer="91"/>
<wire x1="10.16" y1="129.54" x2="20.32" y2="129.54" width="0.1524" layer="91"/>
<pinref part="U2" gate="U$1" pin="GP8"/>
</segment>
</net>
<net name="N$8" class="0">
<segment>
<pinref part="DRIBBLERS" gate="G$1" pin="6"/>
<wire x1="-30.48" y1="129.54" x2="7.62" y2="129.54" width="0.1524" layer="91"/>
<wire x1="7.62" y1="129.54" x2="7.62" y2="127" width="0.1524" layer="91"/>
<wire x1="7.62" y1="127" x2="20.32" y2="127" width="0.1524" layer="91"/>
<pinref part="U2" gate="U$1" pin="GP9"/>
</segment>
</net>
<net name="N$9" class="0">
<segment>
<pinref part="ARMS" gate="G$1" pin="1"/>
<wire x1="-30.48" y1="121.92" x2="20.32" y2="121.92" width="0.1524" layer="91"/>
<pinref part="U2" gate="U$1" pin="GP10"/>
</segment>
</net>
<net name="N$10" class="0">
<segment>
<pinref part="ARMS" gate="G$1" pin="2"/>
<wire x1="-30.48" y1="119.38" x2="20.32" y2="119.38" width="0.1524" layer="91"/>
<pinref part="U2" gate="U$1" pin="GP11"/>
</segment>
</net>
<net name="N$11" class="0">
<segment>
<pinref part="ARMS" gate="G$1" pin="3"/>
<wire x1="-30.48" y1="116.84" x2="20.32" y2="116.84" width="0.1524" layer="91"/>
<pinref part="U2" gate="U$1" pin="GP12"/>
</segment>
</net>
<net name="N$12" class="0">
<segment>
<pinref part="ARMS" gate="G$1" pin="4"/>
<wire x1="-30.48" y1="114.3" x2="20.32" y2="114.3" width="0.1524" layer="91"/>
<pinref part="U2" gate="U$1" pin="GP13"/>
</segment>
</net>
<net name="N$13" class="0">
<segment>
<pinref part="ARMS" gate="G$1" pin="5"/>
<wire x1="-30.48" y1="111.76" x2="15.24" y2="111.76" width="0.1524" layer="91"/>
<wire x1="15.24" y1="111.76" x2="15.24" y2="109.22" width="0.1524" layer="91"/>
<wire x1="15.24" y1="109.22" x2="20.32" y2="109.22" width="0.1524" layer="91"/>
<pinref part="U2" gate="U$1" pin="GP14"/>
</segment>
</net>
<net name="N$14" class="0">
<segment>
<pinref part="ARMS" gate="G$1" pin="6"/>
<wire x1="-30.48" y1="109.22" x2="12.7" y2="109.22" width="0.1524" layer="91"/>
<wire x1="12.7" y1="109.22" x2="12.7" y2="106.68" width="0.1524" layer="91"/>
<wire x1="12.7" y1="106.68" x2="20.32" y2="106.68" width="0.1524" layer="91"/>
<pinref part="U2" gate="U$1" pin="GP15"/>
</segment>
</net>
<net name="N$15" class="0">
<segment>
<pinref part="U2" gate="U$1" pin="GP27"/>
<wire x1="55.88" y1="134.62" x2="101.6" y2="134.62" width="0.1524" layer="91"/>
<pinref part="KICK" gate="G$1" pin="1"/>
</segment>
</net>
<net name="N$16" class="0">
<segment>
<pinref part="R1" gate="G$1" pin="2"/>
<wire x1="91.44" y1="132.08" x2="101.6" y2="132.08" width="0.1524" layer="91"/>
<pinref part="KICK" gate="G$1" pin="2"/>
</segment>
</net>
<net name="N$17" class="0">
<segment>
<pinref part="R2" gate="G$1" pin="2"/>
<pinref part="U2" gate="U$1" pin="GP26"/>
<wire x1="55.88" y1="132.08" x2="76.2" y2="132.08" width="0.1524" layer="91"/>
<wire x1="76.2" y1="132.08" x2="76.2" y2="99.06" width="0.1524" layer="91"/>
<wire x1="76.2" y1="99.06" x2="83.82" y2="99.06" width="0.1524" layer="91"/>
<wire x1="83.82" y1="99.06" x2="91.44" y2="99.06" width="0.1524" layer="91"/>
<wire x1="91.44" y1="99.06" x2="99.06" y2="99.06" width="0.1524" layer="91"/>
<wire x1="99.06" y1="99.06" x2="99.06" y2="96.52" width="0.1524" layer="91"/>
<pinref part="D1" gate="G$1" pin="C"/>
<junction x="91.44" y="99.06"/>
<wire x1="91.44" y1="104.14" x2="91.44" y2="99.06" width="0.1524" layer="91"/>
<pinref part="R3" gate="G$1" pin="P$1"/>
<pinref part="R3" gate="G$1" pin="P$2"/>
<wire x1="86.36" y1="111.76" x2="83.82" y2="111.76" width="0.1524" layer="91"/>
<wire x1="83.82" y1="111.76" x2="83.82" y2="99.06" width="0.1524" layer="91"/>
<junction x="83.82" y="99.06"/>
</segment>
</net>
<net name="AGND" class="0">
<segment>
<pinref part="R2" gate="G$1" pin="1"/>
<wire x1="91.44" y1="88.9" x2="91.44" y2="86.36" width="0.1524" layer="91"/>
<pinref part="SUPPLY1" gate="G$1" pin="AGND"/>
</segment>
<segment>
<pinref part="D1" gate="G$1" pin="A"/>
<wire x1="99.06" y1="91.44" x2="99.06" y2="86.36" width="0.1524" layer="91"/>
<pinref part="SUPPLY2" gate="G$1" pin="AGND"/>
</segment>
<segment>
<pinref part="TOFS" gate="G$1" pin="2"/>
<pinref part="SUPPLY3" gate="G$1" pin="AGND"/>
</segment>
<segment>
<pinref part="SUPPLY4" gate="G$1" pin="AGND"/>
<pinref part="DRIBBLERS_PWM" gate="G$1" pin="2"/>
</segment>
<segment>
<pinref part="SUPPLY5" gate="G$1" pin="AGND"/>
<pinref part="ARMS_PWM" gate="G$1" pin="2"/>
</segment>
<segment>
<pinref part="U2" gate="U$1" pin="GND"/>
<pinref part="SUPPLY6" gate="G$1" pin="AGND"/>
</segment>
<segment>
<pinref part="KICK" gate="G$1" pin="3"/>
<pinref part="SUPPLY7" gate="G$1" pin="AGND"/>
</segment>
</net>
<net name="VCC" class="0">
<segment>
<pinref part="TOFS" gate="G$1" pin="1"/>
<wire x1="-15.24" y1="160.02" x2="-12.7" y2="160.02" width="0.1524" layer="91"/>
<label x="-12.7" y="160.02" size="1.778" layer="95"/>
</segment>
<segment>
<wire x1="-45.72" y1="152.4" x2="-43.18" y2="152.4" width="0.1524" layer="91"/>
<label x="-43.18" y="152.4" size="1.778" layer="95"/>
<pinref part="DRIBBLERS_PWM" gate="G$1" pin="1"/>
</segment>
<segment>
<wire x1="-33.02" y1="99.06" x2="-30.48" y2="99.06" width="0.1524" layer="91"/>
<label x="-30.48" y="99.06" size="1.778" layer="95"/>
<pinref part="ARMS_PWM" gate="G$1" pin="1"/>
</segment>
<segment>
<label x="58.42" y="165.1" size="1.778" layer="95"/>
</segment>
</net>
<net name="N$18" class="0">
<segment>
<pinref part="U2" gate="U$1" pin="GP21"/>
<wire x1="55.88" y1="121.92" x2="63.5" y2="121.92" width="0.1524" layer="91"/>
<pinref part="I2C" gate="G$1" pin="1"/>
</segment>
</net>
<net name="N$19" class="0">
<segment>
<pinref part="U2" gate="U$1" pin="GP20"/>
<wire x1="55.88" y1="119.38" x2="63.5" y2="119.38" width="0.1524" layer="91"/>
<pinref part="I2C" gate="G$1" pin="2"/>
</segment>
</net>
<net name="N$20" class="0">
<segment>
<pinref part="R1" gate="G$1" pin="1"/>
<wire x1="91.44" y1="121.92" x2="91.44" y2="119.38" width="0.1524" layer="91"/>
<pinref part="R3" gate="G$1" pin="P$3"/>
</segment>
</net>
<net name="N$21" class="0">
<segment>
<pinref part="U2" gate="U$1" pin="VBUS"/>
<wire x1="55.88" y1="165.1" x2="58.42" y2="165.1" width="0.1524" layer="91"/>
</segment>
</net>
</nets>
</sheet>
</sheets>
</schematic>
</drawing>
<compatibility>
<note version="8.2" severity="warning">
Since Version 8.2, EAGLE supports online libraries. The ids
of those online libraries will not be understood (or retained)
with this version.
</note>
<note version="8.3" severity="warning">
Since Version 8.3, EAGLE supports URNs for individual library
assets (packages, symbols, and devices). The URNs of those assets
will not be understood (or retained) with this version.
</note>
<note version="8.3" severity="warning">
Since Version 8.3, EAGLE supports the association of 3D packages
with devices in libraries, schematics, and board files. Those 3D
packages will not be understood (or retained) with this version.
</note>
</compatibility>
</eagle>
