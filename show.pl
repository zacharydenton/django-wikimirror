#!/usr/bin/perl -w
use strict;
use Cwd 'abs_path';
use File::Basename;

sub LooseEntities {
	$_ = $_[0];
	s/&lt;/</g;
	s/&gt;/>/g;
	s/&apos;/'/g;
	s/&quot;/"/g;
	s/&amp;/\&/g;
	return $_;
}

sub ShowTopic {
	(my $found, my $foundLine, my $source) = @_;
	my $regexp = $foundLine;
	open RESULT, ">/var/tmp/result.$$";
	print RESULT "$foundLine\n";
	my $getText = 0;
	my $insideText = 0;
	my $foundEndText = 0;
    my $findNextCounter = 0;
	while(1) {
		open XML, "bzip2 -cd \"$found\" |";
		while(<XML>) {
			if (/<title>\Q$regexp\E<\/title>/) {
				$getText = 1;
			}
			elsif (/<title>/) {
				$getText = 0;
			}

			if ($getText) {
				if (/<text ?[^>]*>(.*)<\/text>/) {
					print RESULT LooseEntities($1)."\n"; 
					$getText = 0; 
					$foundEndText = 1;
				} 
				elsif (/<text ?[^>]*>(.*)/) {
					print RESULT LooseEntities($1)."\n"; 
					$insideText = 1; 
				}
				elsif (($insideText) && (/(.*?)<\/text>$/)) {
					print RESULT LooseEntities($1)."\n";
					$insideText = 0;
					$getText = 0;
					$foundEndText = 1;
				} elsif ($insideText) {
					print RESULT LooseEntities($_);
				}
			}
		}
		close XML;
		if ($foundEndText) {
			last;
		} else {
			# Need the rest from the next bzip2 volume
            if ($findNextCounter > 5) {
                last;
            } else {
			    $found =~ m/rec(\d\d\d\d\d)/;
			    my $nextNum = $1 + 1;
			    $nextNum = sprintf "%05d", $nextNum;
			    $found =~ s/rec\d\d\d\d\d/rec$nextNum/;
                $findNextCounter += 1;
            }
		}
	}
	close RESULT;
	my $path = dirname(abs_path($0));
    system("cd $path/mediawiki_sa/ && php testparser.php /var/tmp/result.$$ $source > /var/tmp/result.$$.html");
	return "/var/tmp/result.$$.html";
}

die "Usage: $0 file.bz2 title source\n"
unless @ARGV == 3;

print ShowTopic($ARGV[0], $ARGV[1], $ARGV[2]) . "\n";
