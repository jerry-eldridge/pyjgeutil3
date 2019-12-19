
def BMI(mass_lb,height_in):
    return 703.0*mass_lb/(height_in)**2
def Status(bmi):
    if bmi < 15:
        s = 'Very severely underweight'
        return s
    elif bmi <= 16.0:
        s = 'Severely underweight'
        return s
    elif bmi <= 18.5:
        s = 'Underweight'
        return s
    elif bmi <= 25:
        s = 'Normal (healthy weight)'
        return s
    elif bmi <= 30:
        s = 'Overweight'
        return s
    elif bmi <= 35:
        s = 'Obese I (Moderately obese)'
        return s
    elif bmi <= 40:
        s = 'Obese II (Severely obese)'
        return s
    elif bmi > 40:
        s = 'Obese III (Very severely obese)'
        return s

def Mass_kg(mass_lb):
    return 0.453592*mass_lb
def Height_cm(height_in):
    return 2.54*height_in

def Newtons(mass_kg):
    return 9.80665*mass_kg

def BodyFat(bmi, age, sex, maturity):
    if maturity==child:
        return 1.51*bmi - 0.70*age - 3.6*sex + 1.4
    elif maturity==adult:
        return 1.20*bmi + 0.23*age - 10.8*sex - 5.4

def BMR_Mifflin(mass_lb, height_in, age_year, sex):
    m = Mass_kg(mass_lb)
    h = Height_cm(height_in)
    a = age_year
    if sex == male:
        s = 5
    elif sex == female:
        s = -161
    P = 10.0*m + 6.25*h - 5.0*a + s
    bmr = P
    return bmr

def IdealBodyWeight(height_in, sex):
    if sex == male:
        kg = 50 + 2.3*(height_in-60)
    elif sex == female:
        kg = 45.5 + 2.3*(height_in-60)
    lbs = kg/0.453592
    return lbs

child = 0
adult = 1 # adult is 1 child is 0
male = 1
female = 0

def HealthDemo(mass_lb_cur=208,height_in=5*12+8,age=49,maturity=adult,sex=male,lbs_hi=205,lbs_lo=150,
               step = 1):

    #sex = male # male is 1 female is 0

    M = range(lbs_hi,lbs_lo,-1*abs(step))

    s = '%5s %7s %7s %7s %7s %12s %8s %7s %7s' % ('lb','kg','N',"%Fat","BMI","Status","LbsOver","BMR","Goal")
    print s
    print 'x'*75
    for mass_lb in M:
        bmi = BMI(mass_lb,height_in)
        status = Status(bmi)
        kg = Mass_kg(mass_lb)
        N = Newtons(kg)
        body_fat = BodyFat(bmi,age,sex,adult)
        bmr = BMR_Mifflin(mass_lb, height_in, age, sex)
        goal = bmr-500
        ibw = IdealBodyWeight(height_in, sex)
        LbsOver = mass_lb - ibw
        s = '%5d %7.2f %7.1f %7.2f %7.3f %12s %8.1f %7.2f %7.2f' % (mass_lb, kg, N, body_fat, bmi, status[:12], LbsOver, bmr, goal)
        print s
        if mass_lb == mass_lb_cur:
            s = '&'*75
        else:
            s = '-'*75
        print s
    return


#HealthDemo()

