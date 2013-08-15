function validatePreferences() 
{
	errors = false;
	//Get current Form
	form = document.getElementById('edit');
	//Get Form Fields
	pwd = document.getElementsByName('util_user_pwd')[0];
	lbl_pwd = getLabel('util_user_pwd');
	pwd_confirm = document.getElementsByName('util_user_pwd_confirm')[0];
	lbl_pwd_confirm = getLabel('util_user_pwd_confirm');
	//Clear all warnings
	resetField(pwd,lbl_pwd);
	resetField(pwd_confirm,lbl_pwd_confirm);
	//Check whether all mandatory fields are filled or not
	if (isSameValue(pwd,lbl_pwd,pwd_confirm,lbl_pwd_confirm,_("Passwords do not match."))) errors = true;
	return errors;
}
