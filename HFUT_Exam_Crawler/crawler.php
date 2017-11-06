<?php
require 'vendor/autoload.php';

/* Subject选项：
	毛中特: mzdsxhzgteshzylltx
	马克思: marxism
	近代史: zgjdsgy
	思修: sxddxyyfljc
*/
/* Chapter选项:
	毛中特: 1-12
	马克思: 0-7
	近代史: 1-7
	思修: 0-7
*/

$Options = array(
	'Chapter'=>5,
	'Subject'=>'mzdsxhzgteshzylltx',
	'Uid'=>'2014218000'
);

$db = mysqli_connect("127.0.0.1", "root", "123", "exam") or die("Couldn't connect database");
mysqli_query($db, "set names utf8");

function crawler() {
	global $Options;
	if($Options['Subject'] == 'mzdsxhzgteshzylltx') {
		if($Options['Chapter'] > 7)
			$EXAM_URL="10.111.100.107/exercise/singleChapter.asp?subtable=mzdsxhzgteshzylltx2&chapter=" . strval($Options['Chapter']-7) ."&sid=$Options[Uid]";
		else
			$EXAM_URL="10.111.100.107/exercise/singleChapter.asp?subtable=mzdsxhzgteshzylltx1&chapter=$Options[Chapter]&sid=$Options[Uid]";
	}
	else
		$EXAM_URL="10.111.100.107/exercise/singleChapter.asp?subtable=$Options[Subject]&chapter=$Options[Chapter]&sid=$Options[Uid]";

	// echo $EXAM_URL;

	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $EXAM_URL);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	$out = curl_exec($ch);
	curl_close($ch);
	$out = iconv("gb2312", "utf8", $out);
	return $out;
}

function get_data() {
	global $Options;
	global $db;

	$html = new simple_html_dom();
	$html->load(crawler());
	$data = $html->find('body table tbody tr td form table tbody tr input[type=hidden]');
	// echo $html;

	foreach($data as $input) {
		if(substr($input->id, 0, 4) == 'cent') continue;
		if(substr($input->id, 0, 3) == 'ans') {
			// do something...
			$ans = $input->value;
			if(isset($a)) {
				if(strlen($ans) == 1)
					$type = 2; // 单选
				else
					$type = 3; // 多选
			}
			else
				$type = 1; // 判断

			if($type == 1) {
				$sql = "INSERT INTO `exam`.`$Options[Subject]`
					(`id`, `type`, `subject`, `a`, `b`, `c`, `d`, `answer`, `chapter`) VALUES
					(NULL, '1', '$ques', NULL, NULL, NULL, NULL, '$ans', '$Options[Chapter]')";
			} else {
				$sql = "INSERT INTO `exam`.`$Options[Subject]`
					(`id`, `type`, `subject`, `a`, `b`, `c`, `d`, `answer`, `chapter`) VALUES
					(NULL, '$type', '$ques', '$a', '$b', '$c', '$d', '$ans', '$Options[Chapter]')";
			}

			// echo "$sql<br>";
			mysqli_query($db, $sql);

			// echo "Type: $type<br>";
			// echo "Ques: $ques<br>";
			// echo "A. $a<br>";
			// echo "B. $b<br>";
			// echo "C. $c<br>";
			// echo "D. $d<br>";
			// echo "Ans: $ans<br>";

			$type = $ques = $a = $b = $c = $d = $ans = NULL;
			continue;
		}

		switch(substr($input->id, 0, 1)) {
			case 'q':
				$ques = $input->value;
				break;
			case 'a':
				$a = $input->value;
				break;
			case 'b':
				$b = $input->value;
				break;
			case 'c':
				$c = $input->value;
				break;
			case 'd':
				$d = $input->value;
				break;
		}
	}
}

// echo crawler();
get_data();
echo "已抓取：" . mysqli_num_rows(mysqli_query($db, "SELECT * FROM  `$Options[Subject]`")) . "条\n";

mysqli_close($db);

