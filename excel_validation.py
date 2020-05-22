import pandas as pd
import re
from pandas_schema import Column, Schema
from pandas_schema.validation import CustomElementValidation
import numpy as np
import requests


#String check
def check_str(st):
    try:
        st = str(st)
        return re.match(r"[A-Za-z0-9!@#$%&\*\.\,\+-_\s]+",st).group()==st
    except:
        return False


def check_mob_number(mob):
    try:
        mob = str(mob)
        mob = mob.replace(' ','')
        mob = mob.replace('-','')
        if mob[0:3]=='+91':
            return (len(mob)==13)and(mob.isnumeric())
        else:
            return (len(mob)==10)and(mob.isnumeric())
    except:
        return False

def check_pincode(pincode):
    try:
        pincode = str(pincode)
        pincode = pincode.replace(' ','')
        pincode = pincode.replace('-','')
        return (len(pincode)==6)and(pincode.isnumeric())
    except:
        return False
def check_dob(date_age):
    try:
        date_age = str(date_age)
        return re.match(r"[A-Za-z0-9!@#$%\\&\*\.\,\+-_\s]+",date_age).group()==date_age
    except:
        return False

str_validation = [CustomElementValidation(lambda d: check_str(d), 'invalid String')]
mob_validation = [CustomElementValidation(lambda d: check_mob_number(d), 'invalid mobile number')]
pincode_validation = [CustomElementValidation(lambda d: check_pincode(d), 'invalid pincode')]
null_validation = [CustomElementValidation(lambda d: d is not np.nan, 'this field cannot be null')]
dob_validation = [CustomElementValidation(lambda d: check_dob(d), 'either date or age is not valid')]

def function_validation(filename,cand_stage):
    df= pd.read_excel(filename,sheet_name='Mobilizer')
    df = df.fillna('')
    #print(df.columns)
    df['date_age']=df['Age*']+df['Date of Birth*'].astype(str)

    if cand_stage==str(1):
        schema = Schema([
            #nan check column non mandate
            Column('Candidate Photo',null_validation),
            Column('Middle Name',null_validation),
            Column('Last Name',null_validation),
            Column('Secondary Contact  No',null_validation),
            Column('Email id',null_validation),
            Column('Present Panchayat',null_validation),
            Column('Present Taluk/Block',null_validation),
            Column('Present Address line1',null_validation),
            Column('Present Address line2',null_validation),
            Column('Present Village',null_validation),
            Column('Permanent Address line1',null_validation),
            Column('Permanent Address line2',null_validation),
            Column('Permanent Village',null_validation),
            Column('Permanent Panchayat',null_validation),
            Column('Permanent Taluk/Block',null_validation),
            #str+null check
            Column('Fresher/Experienced?*',str_validation + null_validation),
            Column('Salutation*',str_validation + null_validation),
            Column('First Name*',str_validation + null_validation),
            Column('Gender*',str_validation + null_validation),
            Column('Marital Status*',str_validation + null_validation),
            Column('Caste*',str_validation + null_validation),
            Column('Disability Status*',str_validation + null_validation),
            Column('Religion*',str_validation + null_validation),
            Column('Source of Information*',str_validation + null_validation),
            Column('Present District*',str_validation + null_validation),
            Column('Present State*',str_validation + null_validation),
            Column('Present Country*',str_validation + null_validation),
            Column('Permanent District*',str_validation + null_validation),
            Column('Permanent State*',str_validation + null_validation),
            Column('Permanent Country*',str_validation + null_validation),
            #pincode check
            Column('Present Pincode*',pincode_validation + null_validation),
            Column('Permanent Pincode*',pincode_validation + null_validation),
            #mobile number check
            Column('Primary contact  No*',mob_validation + null_validation),
            #date of birth and age pass(null check)
            Column('Date of Birth*',null_validation),
            Column('Age*',null_validation),
            Column('date_age',dob_validation)
            ])
    errors = schema.validate(df)
    errors_index_rows = [e.row for e in errors]

    pd.DataFrame({'col':errors}).to_csv('errors.csv')
    df_clean = df.drop(index=errors_index_rows)
    df_clean.to_csv('clean_data.csv',index=None)
    return (len(errors_index_rows))
   

"""
def pincode(pincode):
    r=requests.get('https://api.postalpincode.in/pincode/'+pincode)
for i in df['Pincode*'].unique():
	print(i,end=',')
	if i !='':
		r = requests.get('https://api.postalpincode.in/pincode/'+str(i)).json()[0]
		if r["Status"]=="Error":
			print('invalid pincode')
		else:
			r=r['PostOffice'][0]
			pin_data[i]=(r['District'],r['State'],r['Country'])
			print()
"""
