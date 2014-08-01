
soap_checkPrisonerInfo = """\
<?xml version="1.0" encoding="UTF-8"?>
<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:tns="http://prisonvisits.service.gov.uk/booking" xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
<env:Body>
    <tns:checkPrisonerInfo><prisonerInfo><forename>Lynn</forename><surname>Able</surname><number>b2793za</number><prisonId>RCI</prisonId><dateOfBirth>1977-06-15</dateOfBirth></prisonerInfo></tns:checkPrisonerInfo></env:Body></env:Envelope>
"""

soap_getAvailableTimeSlots1 = """\
<?xml version="1.0" encoding="UTF-8"?><env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:tns="http://prisonvisits.service.gov.uk/booking" xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"><env:Body><tns:getAvailableTimeSlots><prisonerInfo><forename>Lynn</forename><surname>Able</surname><number>b2793za</number><prisonId>RCI</prisonId><dateOfBirth>1977-06-15</dateOfBirth></prisonerInfo><visitors><forename>Kimberli</forename><surname>Sevier</surname><dateOfBirth>1992-05-27</dateOfBirth></visitors><startDate>2014-07-21</startDate><endDate>2014-08-14</endDate></tns:getAvailableTimeSlots></env:Body></env:Envelope>
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

soap_bookVisit_fixed = """\
<?xml version="1.0" encoding="UTF-8"?>
<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:tns="http://services.pvb.nomis.syscon.net/" xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
    <env:Body>
        <tns:bookVisit>
            <prisonerInfo>
                <forename>Lynn</forename>
                <surname>Able</surname>
                <dateOfBirth>1977-06-15</dateOfBirth>
                <number>b2793za</number>
                <prisonId>RCI</prisonId>
            </prisonerInfo>
            <visitors>
                <forename>Kimberli</forename>
                <surname>Sevier</surname>
                <dateOfBirth>1992-05-27</dateOfBirth>
            </visitors>
            <timeSlot>
                <startTime>15:00:00</startTime>
                <endTime>17:00:00</endTime>
            </timeSlot>
        </tns:bookVisit>
    </env:Body>
</env:Envelope>
"""
