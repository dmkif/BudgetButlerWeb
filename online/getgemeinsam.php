<?php
require_once('creds.php');
try {
	if( isset($_POST['email']) and isset($_POST['password'])){
		$auth = getAuth();
		$auth->login($_POST['email'], $_POST['password']);
		echo "well done!\r\n\r\n";
		$dbh = getPDO();

		// Test, ob Verknüpfung mit anderer Person gegeben
		$other_person_selected = false;
		$other_person_confirmed = false;
		$other_name = 'undef';

		$sql = 'select DestinationPerson from gemeinsam_zuordnung where SourcePerson = :sourceperson';
		$sth = $dbh->prepare($sql, array(PDO::ATTR_CURSOR => PDO::CURSOR_FWDONLY));
		$sth->execute(array(':sourceperson' => $auth->getUsername()));
		$other = $sth->fetchAll();

		if (sizeof($other) > 0){
			$other_person_selected = true;
			$other_name = array_values($other)[0]['DestinationPerson'];

			$sql = 'select DestinationPerson from gemeinsam_zuordnung where SourcePerson = :sourceperson';
			$sth = $dbh->prepare($sql, array(PDO::ATTR_CURSOR => PDO::CURSOR_FWDONLY));
			$sth->execute(array(':sourceperson' => $other_name));
			$sourceperson = $sth->fetchAll();
			if (sizeof($sourceperson) > 0) {
				$sourceperson_name = array_values($sourceperson)[0]['DestinationPerson'];
				if (strcmp($sourceperson_name, $auth->getUsername()) == 0){
					$other_person_confirmed = true;
				}
			}
		}
		echo '\n\n os:';
		echo $other_person_selected;
		echo '\n\n oc:';
		echo $other_person_confirmed;
		echo '\n\n';
		if ($other_person_confirmed){
			$sql = "SELECT * FROM `gemeinsame_eintraege` WHERE person = :person OR person = :other_person";
			$sth = $dbh->prepare($sql);
			$sth->execute(array(	':person' => $auth->getUsername(),
						':other_person' => $other_name));
			$alldata = $sth->fetchAll();
		}
		else {
			// Wenn nicht gegeben
			$sql = "SELECT * FROM `gemeinsame_eintraege` WHERE person = :person";
			$sth = $dbh->prepare($sql);
			$sth->execute(array(':person' => $auth->getUsername()));
			$alldata = $sth->fetchAll();
		}

		$result = "#######MaschinenimportStart\r\nDatum,Kategorie,Name,Wert,Person,Dynamisch";
		foreach($alldata as $item) {
			$row = $item['datum'].','.str_replace(',',' ',$item['kategorie']).','.str_replace(',',' ',$item['name']).','.str_replace(',','.',$item['wert']). ','. str_replace(',','.',$item['person']).',False';
			$result = $result."\r\n".$row;
		}
		$result = $result."\n#######MaschinenimportEnd\r\n\r\n";
		echo $result;
	}
}
catch (\Delight\Auth\InvalidEmailException $e) {
    // wrong email address
    echo "wrong email";
}
catch (\Delight\Auth\InvalidPasswordException $e) {
	echo "wrong pass";
}
catch (\Delight\Auth\EmailNotVerifiedException $e) {
    // email not verified
	echo "email not verified";
}
catch (\Delight\Auth\TooManyRequestsException $e) {
    // too many requests
    echo "too many requests";
}


?>
