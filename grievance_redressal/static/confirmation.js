function isChecked()
{
    if (document.getElementById('agree').checked) {
	document.getElementById('confirm').disabled = false;
    }

    if (!document.getElementById('agree').checked) {
	document.getElementById('confirm').disabled = true;
    }
}
