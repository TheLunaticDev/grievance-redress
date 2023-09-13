function isChecked()
{
    if (document.getElementById('agree').checked) {
	document.getElementById('edit').hidden = true;
	document.getElementById('confirm').hidden = false;
	document.getElementById('confirm').disabled = false;
    }

    if (!document.getElementById('agree').checked) {
	document.getElementById('confirm').hidden = true;
	document.getElementById('confirm').disabled = true;
	document.getElementById('edit').hidden = false;
    }
}
