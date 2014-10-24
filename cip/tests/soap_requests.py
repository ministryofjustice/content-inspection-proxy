
soap_checkPrisonerInfo = """\
<?xml version="1.0" encoding="UTF-8"?>
<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:tns="http://services.pvb.nomis.syscon.net/"
        xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
    <env:Body>
        <tns:checkPrisonerInfo>
            <prisonerInfo>
                <forename>Jilly</forename>
                <surname>Hall</surname>
                <dateOfBirth>1970-01-01T00:00:00</dateOfBirth>
                <number>a1401ae</number>
                <prisonId>LEI</prisonId>
            </prisonerInfo>
        </tns:checkPrisonerInfo>
    </env:Body>
</env:Envelope>
"""

soap_getAvailableTimeSlots1 = """\
<?xml version="1.0" encoding="UTF-8"?>
<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:tns="http://services.pvb.nomis.syscon.net/"
        xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
    <env:Body>
        <tns:getAvailableTimeSlots>
            <prisonerInfo>
                <forename>Jilly</forename>
                <surname>Hall</surname>
                <dateOfBirth>1970-01-01T00:00:00</dateOfBirth>
                <number>a1401ae</number>
                <prisonId>LEI</prisonId>
            </prisonerInfo>
            <visitors>
                <dateOfBirth>1976-04-30T00:00:00</dateOfBirth>
                <forename>Tinker</forename>
                <surname>Bell</surname>
            </visitors>
            <startDate>2014-10-21T00:00:00</startDate>
            <endDate>2014-10-21T01:00:00</endDate>
        </tns:getAvailableTimeSlots>
    </env:Body>
</env:Envelope>
"""

soap_getAvailableTimeSlots2 = """\
<?xml version="1.0" encoding="UTF-8"?><env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:tns="http://prisonvisits.service.gov.uk/booking" xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"><env:Body><tns:getAvailableTimeSlots><prisonerInfo><forename>Lynn</forename><surname>Able</surname><number>b2793za</number><prisonId>RCI</prisonId><dateOfBirth>1977-06-15</dateOfBirth></prisonerInfo><visitors><forename>Kimberli</forename><surname>Sevier</surname><dateOfBirth>1992-05-27</dateOfBirth></visitors><startDate>2014-07-21</startDate><endDate>2014-08-14</endDate></tns:getAvailableTimeSlots></env:Body></env:Envelope>
"""

soap_bookVisit = """\
<?xml version="1.0" encoding="UTF-8"?>
<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:tns="http://prisonvisits.service.gov.uk/booking" xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
    <env:Body>
        <tns:bookVisit>
            <prisonerInfo>
                <forename>Lynn</forename>
                <surname>Able</surname>
                <number>b2793za</number>
                <prisonId>RCI</prisonId>
                <dateOfBirth>1977-06-15</dateOfBirth>
            </prisonerInfo>
            <visitors>
                <forename>Kimberli</forename>
                <surname>Sevier</surname>
                <dateOfBirth>1992-05-27</dateOfBirth>
            </visitors><timeSlot>
            <startTime>15:00:00</startTime>
                <endTime>17:00:00</endTime>
            </timeSlot>
        </tns:bookVisit>
    </env:Body>
</env:Envelope>
"""
#
# soap_bookVisit_fixed = """\
# <?xml version="1.0" encoding="UTF-8"?>
# <env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:tns="http://services.pvb.nomis.syscon.net/" xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
#     <env:Body>
#         <tns:bookVisit>
#             <prisonerInfo>
#                 <forename>Lynn</forename>
#                 <surname>Able</surname>
#                 <dateOfBirth>1977-06-15</dateOfBirth>
#                 <number>b2793za</number>
#                 <prisonId>RCI</prisonId>
#             </prisonerInfo>
#             <visitors>
#                 <forename>Kimberli</forename>
#                 <surname>Sevier</surname>
#                 <dateOfBirth>1992-05-27</dateOfBirth>
#             </visitors>
#             <timeSlot>
#                 <startTime>15:00:00</startTime>
#                 <endTime>17:00:00</endTime>
#             </timeSlot>
#         </tns:bookVisit>
#     </env:Body>
# </env:Envelope>
# """

soap_bookVisit_long = """\
<?xml version="1.0" encoding="UTF-8"?>
<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:tns="http://services.pvb.nomis.syscon.net/" xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
    <env:Body>
        <tns:bookVisit>
            <prisonerInfo>
                <forename>Lynn</forename>
                <surname>Able</surname>
                <dateOfBirth>1977-06-15T00:00:00</dateOfBirth>
                <number>b2793za</number>
                <prisonId>RCI</prisonId>
            </prisonerInfo>
            <visitors>
                <dateOfBirth>1977-06-15T00:00:00</dateOfBirth>
                <forename>Kimberli</forename>
                <surname>12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890</surname>
            </visitors>
            <timeSlot>
                <startTime>2014-01-01T15:00:00</startTime>
                <endTime>2014-01-01T17:00:00</endTime>
            </timeSlot>
        </tns:bookVisit>
    </env:Body>
</env:Envelope>
"""

soap_bookVisit_fixed = """\
<?xml version="1.0" encoding="UTF-8"?>

<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:tns="http://services.pvb.nomis.syscon.net/" xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
    <env:Body>
        <tns:bookVisit>
            <prisonerInfo>
                <forename>Lynn</forename>
                <surname>Able</surname>
                <dateOfBirth>1977-06-15T00:00:00</dateOfBirth>
                <number>b2793za</number>
                <prisonId>RCI</prisonId>
            </prisonerInfo>
            <visitors>
                <dateOfBirth>1977-06-15T00:00:00</dateOfBirth>
                <forename>Kimberli</forename>
                <surname>Sevier</surname>
            </visitors>
            <timeSlot>
                <startTime>2014-01-01T15:00:00</startTime>
                <endTime>2014-01-01T17:00:00</endTime>
            </timeSlot>
        </tns:bookVisit>
    </env:Body>
</env:Envelope>
"""

soap_bookVisit_expansion = """\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY ha "Ha !">
<!ENTITY ha2 "&ha; &ha;">
<!ENTITY ha3 "&ha2; &ha2;">
<!ENTITY ha4 "&ha3; &ha3;">
<!ENTITY ha5 "&ha4; &ha4;">
]>
<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:tns="http://services.pvb.nomis.syscon.net/" xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
    <env:Body>
        <tns:bookVisit>
            <prisonerInfo>
                <forename>Lynn</forename>
                <surname><root> &ha5; </root></surname>
                <dateOfBirth>1977-06-15T00:00:00</dateOfBirth>
                <number>b2793za</number>
                <prisonId>RCI</prisonId>
            </prisonerInfo>
            <visitors>
                <dateOfBirth>1977-06-15T00:00:00</dateOfBirth>
                <forename>Kimberli</forename>
                <surname>Sevier</surname>
            </visitors>
            <timeSlot>
                <startTime>2014-01-01T15:00:00</startTime>
                <endTime>2014-01-01T17:00:00</endTime>
            </timeSlot>
        </tns:bookVisit>
    </env:Body>
</env:Envelope>
"""



soap_domis_checkPrisonerInfo = """\
<?xml version="1.0" encoding="UTF-8"?>
<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:tns="http://prisonvisits.service.gov.uk/booking"
        xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
    <env:Body>
        <tns:checkPrisonerInfo>
            <prisonerInfo>
                <forename>Lynn</forename>
                <surname>Able</surname>
                <dateOfBirth>1977-06-15T00:00:00</dateOfBirth>
                <number>b2793za</number>
                <prisonId>RCI</prisonId>
            </prisonerInfo>
        </tns:checkPrisonerInfo>
    </env:Body>
</env:Envelope>
"""

soap_domis_getAvailableTimeSlots1 = """\
<?xml version="1.0" encoding="UTF-8"?>
<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:tns="http://prisonvisits.service.gov.uk/booking"
        xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
    <env:Body>
        <tns:getAvailableTimeSlots>
            <prisonerInfo>
                <forename>Jilly</forename>
                <surname>Hall</surname>
                <dateOfBirth>1970-01-01T00:00:00</dateOfBirth>
                <number>a1401ae</number>
                <prisonId>LEI</prisonId>
            </prisonerInfo>
            <visitors>
                <dateOfBirth>1976-04-30T00:00:00</dateOfBirth>
                <forename>Tinker</forename>
                <surname>Bell</surname>
            </visitors>
            <startDate>2014-10-21T00:00:00</startDate>
            <endDate>2014-10-21T01:00:00</endDate>
        </tns:getAvailableTimeSlots>
    </env:Body>
</env:Envelope>
"""
