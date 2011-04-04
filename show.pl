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
	(my $found, my $foundLine) = @_;
	my $regexp = $foundLine;
	open RESULT, ">/tmp/result.$$";
	print RESULT "$foundLine\n";
	my $getText = 0;
	my $insideText = 0;
	my $foundEndText = 0;
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
			$found =~ m/rec(\d\d\d\d\d)/;
			my $nextNum = $1 + 1;
			$nextNum = sprintf "%05d", $nextNum;
			$found =~ s/rec\d\d\d\d\d/rec$nextNum/;
		}
	}
	close RESULT;
	my $path = dirname(abs_path($0));
	system("cd $path/mediawiki_sa/ && php5 testparser.php /tmp/result.$$ > /tmp/result.$$.html");
	if (($? == -1) || ($? & 127) || ($? >> 8)) {
		print "#### mediawiki_sa parser failed! report to woc.fslab.de ####\n";
		open FALLBACK, ">/tmp/result.$$.html";
		print FALLBACK "<html><head><title>woc.fslab.de parser failed - report it!</title></head>\n<body>\n";
		print FALLBACK "<h2>woc.fslab.de parser failed, please report this content (/tmp/result.$$) to them!</h2>";
		open DATA, "/tmp/result.$$";
		while(<DATA>) {
			chomp;
			print FALLBACK $_."<BR/>\n";
		}
		close DATA;
		print FALLBACK "</body>\n</html>\n";
		close FALLBACK;
	}

	return "/tmp/result.$$.html";
}

die "Usage: $0 file.bz2 title\n"
unless @ARGV == 2;

print ShowTopic($ARGV[0], $ARGV[1]) . "\n";
