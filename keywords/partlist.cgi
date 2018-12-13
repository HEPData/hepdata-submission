#!/usr/bin/perl
use CGI qw ( param header p);;

#print header('text/html');

open YAML,'<part.yaml';
$line=<YAML>;
$line=<YAML>;
$n=0;
while ($line=<YAML>){
    if($line=~m/\s+-\s+\{name:/){
        chomp $line;
        if($line=~m/^\s*-\s*{name:\s*(.*),\s*aliases:\s*\[\'(.*)\'\],\s*description:\s*'(.*)'}\s*$/){
            $part[$nclass][++$npart[$nclass]]=$1;
            $alias[$nclass][$npart[$nclass]]=$2;
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
close YAML;
print "<body>\n";

print "<head>\n";
print "<h2>Table of Particle Names</h2>\n";
foreach $nc (1...$nclass){
    print "[<a href='#$class[$nc]'><font size='-1'>$class[$nc]</font></a>]"
}
print "</table>\n";
print "<table border='1' cellpadding='5'>\n";
foreach $nc (1...$nclass){
    print "<tr><td colspan='3' align='center'><b><a name='$class[$nc]' href='#$class[$nc]'>$class[$nc]</a></b>";
    print " (<a href='partlist'>back to top</a>)</td></tr>\n";
print "<tr><th>Particle Name</th><th>Aliases</th><th>Description</th></tr>\n";
    foreach $np (1...$npart[$nc]){
        print "<tr>\n";
        print "<td><font size='-1'>$part[$nc][$np]</font></td>";
        print "<td><font size='-1'>$alias[$nc][$np]</font></td>";
        print "<td><font size='-1'>$desc[$nc][$np]</font></td>";
        print "</tr>\n";
    }
}

print "</table>\n";

print "</body>\n";
