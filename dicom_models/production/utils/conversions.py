# Copyright (c) 2012, The Children's Hospital of Philadelphia
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#    disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#    following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.from datetime import datetime

# source: http://www.google.com/search?q=days+in+year
# source: http://www.google.com/search?q=days+in+month
DAYS_IN_YEAR = 365.242199
DAYS_IN_MONTH = 30.4368499

def days_to_years(days):
    """Converts the value of days into years floating point.

    >>> from decimal import Decimal
    >>> days_to_years(3829)
    10.483454569278836
    >>> days_to_years('3829')
    10.483454569278836
    >>> days_to_years(Decimal('3829'))
    10.483454569278836
    >>> days_to_years(-3829)
    >>> days_to_years('-3829')
    >>> days_to_years(Decimal('-3829'))
    >>> days_to_years(None)
    """
    if days is None:
        return
    days = float(str(days))
    if days < 0:
        return
    return days / DAYS_IN_YEAR

def days_to_age(days, min_years=3, to_string=True):
    """Converts the value of days into an age in years.

    >>> from decimal import Decimal
    >>> days_to_age(3829)
    '10y, 5m'
    >>> days_to_age('3829')
    '10y, 5m'
    >>> days_to_age(Decimal('3829'))
    '10y, 5m'
    >>> days_to_age(393)
    '12m'
    >>> days_to_age(3)
    'Newborn'
    >>> days_to_age(3829, min_years=11)
    '125m'
    >>> days_to_age(3829, to_string=False)
    10.483454569278836
    >>> days_to_age(-3829)
    >>> days_to_age('-3829')
    >>> days_to_age(Decimal('-3829'))
    >>> days_to_age(None)
    """
    if days is None:
        return
    # handles Decimal type
    days = float(str(days))
    if days < 0:
        return

    if not to_string:
        return days / DAYS_IN_YEAR

    if (days // DAYS_IN_YEAR) < min_years:
        mths = int(days // DAYS_IN_MONTH)
        if mths == 0:
            return 'Newborn'
        return '%sm' % mths

    yrs = int(days // DAYS_IN_YEAR)
    mths = int((days % DAYS_IN_YEAR) // DAYS_IN_MONTH)

    if yrs > 0 and mths == 12:
        yrs += 1
        mths = 0

    if mths > 0:
        return '%sy, %sm' % (yrs, mths)
    return '%sy' % yrs

def years_to_age(years, min_years=3, to_string=True):
    """Converts the value of years into an age in years.

    >>> from decimal import Decimal
    >>> years_to_age(7.2)
    '7y, 2m'
    >>> years_to_age('7.2')
    '7y, 2m'
    >>> years_to_age(Decimal('7.2'))
    '7y, 2m'
    >>> years_to_age(4.5, to_string=False)
    4.5
    >>> years_to_age(72)
    '72y'
    >>> years_to_age('2.99')
    '35m'
    >>> years_to_age('3.0')
    '3y'
    >>> years_to_age('0.083')
    'Newborn'
    >>> years_to_age('0.084')
    '1m'
    >>> years_to_age(-7.2)
    >>> years_to_age('-7.2')
    >>> years_to_age(Decimal('-7.2'))
    >>> years_to_age(None)
    """
    if years is None:
        return
    days = float(str(years)) * DAYS_IN_YEAR
    if days < 0:
        return
    return days_to_age(days, min_years, to_string)

def dates_to_age(date1, date2, min_years=3, to_string=True):
    """Calculates an age in years based on two dates.

    >>> from datetime import datetime, date
    >>> dates_to_age(datetime(2002, 2, 14), datetime(2009, 5, 1))
    '7y, 2m'
    >>> dates_to_age(datetime(2009, 5, 1), datetime(2002, 2, 14))
    '7y, 2m'
    >>> dates_to_age(datetime(2002, 2, 14), None)
    >>> dates_to_age(None, datetime(2009, 5, 1))
    >>> dates_to_age(date(2002, 2, 14), date(2009, 5, 1))
    '7y, 2m'
    >>> dates_to_age(date(2009, 5, 1), date(2002, 2, 14))
    '7y, 2m'
    >>> dates_to_age(date(2002, 2, 14), None)
    >>> dates_to_age(None, date(2009, 5, 1))
    """
    if date1 is None or date2 is None:
        return
    if date1 > date2:
        date1, date2 = date2, date1
    days = (date2 - date1).days
    return days_to_age(days, min_years, to_string)

if __name__ == '__name__':
    import doctest
    doctest.testmod()
