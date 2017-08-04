#!/usr/bin/perl
use CGI qw ( param header p);;

print header('text/html');
print "<head>\n";
print "<script type='text/javascript' LANGUAGE='JavaScript'>\n";

open YAML,'<part.yaml';
$line=<YAML>;
$line=<YAML>;
$n=0;
while ($line=<YAML>){
    if($line=~m/\s+-\s+\{name:/){
        chomp $line;
        if($line=~m/^\s*-\s*{name:\s*(.*),\s*aliases:\s*(.*),\s*description:\s*'(.*)'}\s*$/){
            $part[$nclass][++$npart[$nclass]]=$1;
            $desc[$nclass][$npart[$nclass]]=$3;
        }
    } else {
        chomp $line;
        if($line=~m/^\s*(.*):\s*$/){
            $class[++$nclass]=$1;
            $npart[$nclass]=0;
        }
    }
}
print "which = new Array(\n";
foreach $nc (1...$nclass){
    print "new Array(\n";
    foreach $np (1...$npart[$nc]){
        if($np==1) { print "new Array('Select'),\n"; }
        $particle=$part[$nc][$np];
        if($desc[$nc][$np] ne "") { $particle=$particle." - ".$desc[$nc][$np]; }
        print "new Array('$particle')";
        if($np==$npart[$nc]) { print "\n"; } else { print ",\n"; }
    }
    if($nc==$nclass) { print ")\n"; } else { print "),\n"; }

}
print ")";
close YAML;

print "\n"; 
print "function fillSelectFromArray(selectCtrl, itemArray, goodPrompt, badPrompt, defaultItem) {\n";
print "  var i, j;\n";
print "  var prompt;\n";
print "  // empty existing items\n";
print "  for (i = selectCtrl.options.length; i >= 0; i--) {\n";
print "    selectCtrl.options[i] = null;\n";
print "  }\n";
print "  prompt = (itemArray != null) ? goodPrompt : badPrompt;\n";
print "  if (prompt == null) {\n";
print "    j = 0;\n";
print "  }\n";
print "  else {\n";
print "    selectCtrl.options[0] = new Option(prompt);\n";
print "    j = 1;\n";
print "  }\n";
print "  if (itemArray != null) {\n";
print "     // add new items\n";
print "    for (i = 0; i < itemArray.length; i++) {\n";
print "      selectCtrl.options[j] = new Option(itemArray[i][0]);\n";
print "      // the next part allows a second value which will be passed as the arguement Team\n";
print "      if (itemArray[i][1] != null) {\n";
print "         selectCtrl.options[j].value = itemArray[i][1];\n";
print "      }\n";
print "      j++;\n";
print "    }\n";
print "// select first item (prompt) for sub list\n";
print "    selectCtrl.options[0].selected = true\n";
print "  }\n";
print "}\n";
print "//\n";
print "</script>\n";
print "<style>\n";
print " td {font-family:Arial, sans-serif;}\n";
print "</style>\n";
print "</<head>\n";

$change=param("change");
$inex=param("inex");
$nfsp=param("nfsp");
if($change eq "Add FSP") { $nfsp++; }
if($change eq "Remove FSP") { $nfsp--; }

foreach $n (1...$nfsp){
    $fsp[$n]=param("Which$n");
    $mult[$n]=param("mult$n");
    $multtype[$n]=param("multtype$n");
    $oldfsp[$n]=param("oldfsp$n");
    if($fsp[$n] eq "" || $fsp[$n] eq "Select"){ 
        $fsp[$n]=$oldfsp[$n];
    } 
    $group[$n]=param("fsp$n");
}

$beam=param("beam");
$target=param("target");

if($inex eq "inclusive") { $inclusive="checked='checked'"; $exclusive=""}; 
if($inex eq "exclusive") { $exclusive="checked='checked'"; $inclusive=""}; 

print "<p/>";
print "<form method='POST' action='buildreaction.cgi'>";
print "<table cellpadding='10' border='0'>\n";
print "<tr>\n";
print "<td colspan='3'>\n";
print "<h2>HEPData Reactions</h2>";
print "(<a href='part.yaml'>yaml file of particle names</a>)";
print "<br/>\n";
print "(<a href='partlist.cgi'>html file of particle names</a>)";
print "</td></tr>\n";
print "<td>\n";
  print "<table border='0'>\n";
  print "<tr><td colspan='1' align='left'>\n";
  print "Beam Particles";
  print "<select onChange='this.form.submit()' name='beam'>";
  &listpart("beam.list2",$beam);
  print "</select>";
  print "<select onChange='this.form.submit()' name='target'>";
  &listpart("beam.list2",$target);
  print "</select>";
  print "</td>";
  print "</tr>\n";
  print "<tr><td valign='top'>\n";
  print "<table border='0'>";
  print "<tr>\n";
  print "<td>(Selected)</td><td>Final State Particle</td><td>Multiplicity</td></tr>\n";
  foreach $n (1...$nfsp){
      print "<tr>\n";
      $name="fsp"."$n";
      $which="Which"."$n";
      print "<td>\n";
      ($shortfsp,$dummy)=split/\s*-\s*/,$fsp[$n],2;
      print "$n ($shortfsp)</td><td><select name='$name' id='myparton' onclick='fillSelectFromArray(this.form.$which,((this.selectedIndex == -1) ? null : which[this.selectedIndex-1]));'>\n";
      print "<option value='-1'>Select Group\n";
      foreach $type (1...$nclass){
          if($group[$n]==$type1) { print "<option value='$type' selected='selected'>$class[$type]\n";} else { print "<option value='$type'>$class[$type]\n"; }
      }
      print "</select>\n";
      print "<select onChange='this.form.submit()' name='$which' id='myparton' size='1'>\n";
      print "<option> </option>\n";
  
  
      print "</select>\n";
      print "</td>\n";
      print "<td>\n";
      print "<select onChange='this.form.submit()' name='multtype$n'/>\n";
      if($multtype[$n] eq "=") { print "<option selected='selected'>="; } else { print "<option>="; }   
      if($multtype[$n] eq ">") { print "<option selected='selected'>>"; } else { print "<option>>"; }   
      if($multtype[$n] eq "<") { print "<option selected='selected'><"; } else { print "<option><"; }   
      if($multtype[$n] eq ">=") { print "<option selected='selected'>>="; } else { print "<option>>="; }   
      if($multtype[$n] eq "<=") { print "<option selected='selected'><="; } else { print "<option><="; }   
      print "</select>\n";
      print "<select onChange='this.form.submit()' name='mult$n'/>\n";
      if($mult[$n]==1) { print "<option selected='selected'>1"; } else { print "<option>1"; }   
      if($mult[$n]==2) { print "<option selected='selected'>2"; } else { print "<option>2"; }   
      if($mult[$n]==3) { print "<option selected='selected'>3"; } else { print "<option>3"; }   
      if($mult[$n]==4) { print "<option selected='selected'>4"; } else { print "<option>4"; }   
  #    if($mult[$n]==0) { print "<option selected='selected'>'zero'"; } else { print "<option>'zero'"; }   
      print "</select>\n";
      print "</td></tr>\n";
      print "<input type='hidden' name='oldfsp$n' value='$fsp[$n]'/>\n";
      print "<input type='hidden' name='oldmult$n' value='$mult[$n]'/>\n";
      print "<input type='hidden' name='nfsp' value='$nfsp'/>\n";
      print "<input type='hidden' name='obs' value='$obs'/>\n";
    }
  print "</table>\n";
  print "<input onChange='this.form.submit()' type='radio' name='inex' value='inclusive' $inclusive> inclusive or "; 
  print "<input onChange='this.form.submit()' type='radio' name='inex' value='exclusive' $exclusive> exclusive reaction?";
  print "<p/>\n";
  
  print "<input type='submit' name='change' value='Add FSP'/>";
  print "<input type='submit' name='change' value='Remove FSP'/>";
  print "<input type='submit' value='REFRESH'/>\n";
  

  print "</td>\n";
  print "</table>\n";
  print "</form>\n";
  print "<pre>\n";
  print "Reaction: ";
  print "<b><font size='+2'>";
  &doreac;
  print "</font>";
  print "</b>\n";
  print "\n";
  print "</pre>\n";
print "</td>\n";
print "<td valign='top'>\n";
  print "<pre>\n";
  print "<span style='text-decoration: underline;'>Old Input Format:</span>\n";
  print "<b>*reackey: ";
  &doreac;
  print "\n</b>&<b>\n*qual: RE : ";
  &doreac;
  print "</b>\n\n";
  print "</pre>\n";
#print "</td>\n";
#print "<td valign='top'>\n";
  print "<pre>\n";
  print "<span style='text-decoration: underline;'>New YAML Format:</span>\n";
  print "<b>keywords:\n";
  print "  - {name: reactions, values ['";
  &doreac;
  print "']}\n";
  print "</b>&<b>\n";
  print "dependent-variables:\n";
  print "  - header: { name: 'xxxx'}\n";
  print "    qualifiers:\n";
  print "      - { name: 'RE', value: '";
  &doreac;
  print "'}\n";

  print "</pre>\n";
print "</td>\n";
print "</tr>\n";
print "<tr>\n";
print "<td colspan='3'>\n";
print "<a href='observables.html'>link to observables</a>";
print "</td>\n";
print "</tr>\n";
print "</table>\n";


sub varlist{
    my $m=$_[0];
    print "<select onChange='this.form.submit()' name='var$m'>\n";
    foreach $n (1...$nvarlist) {
        if($var[$m] eq "$varlist[$n]"){ 
                print "<option selected='selected'>$varlist[$n]\n"; 
            } 
            else { 
                print "<option >$varlist[$n]\n"; 
            }
        }
    print "</select>\n";
}


sub listpart{
    my $file=$_[0];
    my $select=$_[1];
    open PARTICLES,"<$file";
    while (my $line=<PARTICLES>){
        chomp $line;
        (my $particle,my $id)=split/\t/,$line;
        if($particle eq $select) {print "<option selected='selected'>$particle\n";}
        else { print "<option>$particle\n"; }
        print "</option>\n";
    }
    close PARTICLES
}

sub doreac{
    print "$beam $target -->";
    foreach $n (1...$nfsp){
        print " ";
        ($fsp[$n],$dummy)=split/\s+/,$fsp[$n],2;
        if($multtype[$n] eq ">=" && $mult[$n]==2){
            print "$fsp[$n]S";
        }
        elsif($multtype[$n] eq ">=" && $mult[$n]==1){
            print "$fsp[$n](S)";
        }
        elsif($multtype[$n] eq ">=" && $mult[$n]==0){
            print "($fsp[$n]S)";
        }
        elsif($multtype[$n] eq ">" && $mult[$n]==1){
            print "$fsp[$n]S";
        }
        else{
            if($multtype[$n] ne "="){
               if($multtype[$n] eq '>') { print ".GT.";}  
                if($multtype[$n] eq '<') { print ".LT.";}  
                if($multtype[$n] eq '>=') { print ".GE.";}  
                if($multtype[$n] eq '<=') { print ".LE.";}  
            }
            if($mult[$n]==1 && $multtype[$n] ne "=") { print "$mult[$n]"; }
            if($mult[$n]!=1){ print "$mult[$n]"; }
            print "$fsp[$n]";
        }
    } 
    if($inex eq 'inclusive') { print " X"; }
}
