from django.shortcuts import render
import pyrebase
from django.contrib import  auth as authe
from datetime import datetime
from django.shortcuts import redirect
from web3 import Web3
import json
from django.http import JsonResponse

# Create your views here.

firebaseConfig = {
    'apiKey': "AIzaSyB4bYmDeb3_B0juUAnSyviaRklqv6zKhFQ",
    'authDomain': "djangopyre-7902f.firebaseapp.com",
    'databaseURL': "https://djangopyre-7902f.firebaseio.com",
    'projectId': "djangopyre-7902f",
    'storageBucket': "",
    'messagingSenderId': "358747129386",
    'appId': "1:358747129386:web:642070b5130d61345fa553",
    'measurementId': "G-NHJFCCYS77"
  };

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
web3.eth.defaultAccount = web3.eth.accounts[0]
abi = json.loads('[{"constant":false,"inputs":[{"name":"_batchNumber","type":"int256"},{"name":"_lotNumber","type":"string"}],"name":"BatchtoLot","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_processor","type":"address"},{"name":"_farmer","type":"address"},{"name":"_lotNumber","type":"string"},{"name":"_remarks","type":"string"},{"name":"_receivedShipment","type":"string"}],"name":"addProcessorReport","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_retailer","type":"address"},{"name":"_batchNumber","type":"int256"}],"name":"getRetailerReport","outputs":[{"name":"_productName","type":"string"},{"name":"_remarks","type":"string"},{"name":"_rawMaterial","type":"string"},{"name":"_manufacturedDate","type":"string"},{"name":"_quantity","type":"int256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_processor","type":"address"},{"name":"_farmer","type":"address"},{"name":"_lotNumber","type":"string"}],"name":"getProcessorReport","outputs":[{"name":"_remarks","type":"string"},{"name":"_receivedShipment","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_retailer","type":"address"},{"name":"_retailerKey","type":"string"}],"name":"addRetailer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_processor","type":"address"},{"name":"_processorKey","type":"string"}],"name":"addProcessor","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_farmer","type":"address"},{"name":"_lotNumber","type":"string"}],"name":"getQualityReport","outputs":[{"name":"_remarks","type":"string"},{"name":"_inspector","type":"address"},{"name":"_sampleSize","type":"int256"},{"name":"_defective","type":"int256"},{"name":"_quantity","type":"int256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_farmer","type":"address"},{"name":"_farmerKey","type":"string"}],"name":"addFarmer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_farmer","type":"address"},{"name":"_inspector","type":"address"},{"name":"_lotNumber","type":"string"},{"name":"_remarks","type":"string"},{"name":"_sampleSize","type":"int256"},{"name":"_quantity","type":"int256"},{"name":"_defective","type":"int256"}],"name":"addQualityReport","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_retailer","type":"address"},{"name":"_processor","type":"address"},{"name":"_farmer","type":"address"},{"name":"_remarks","type":"string"},{"name":"_rawMaterial","type":"string"},{"name":"_productName","type":"string"},{"name":"_manufacturedDate","type":"string"},{"name":"_quantity","type":"int256"},{"name":"_batchNumber","type":"int256"}],"name":"addRetailerReport","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_inspector","type":"address"},{"name":"_inspectorKey","type":"string"}],"name":"addInspector","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"name":"farmerAddress","type":"address"},{"indexed":false,"name":"farmerKey","type":"string"}],"name":"farmerAddition","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"processorAddress","type":"address"},{"indexed":false,"name":"processorKey","type":"string"}],"name":"processorAddition","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"retailerAddress","type":"address"},{"indexed":false,"name":"retailerKey","type":"string"}],"name":"retailerAddition","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"inspectoAddress","type":"address"},{"indexed":false,"name":"inspectoKey","type":"string"}],"name":"inspectorAddition","type":"event"}]')
address = web3.toChecksumAddress('0xa6393f6e0514b127c0a662fe039010f633b0945b')


contract = web3.eth.contract(address=address, abi=abi)


firebase =pyrebase.initialize_app(firebaseConfig)
database = firebase.database()
auth = firebase.auth()
def farmer(request):
    sess = request.session['uid']

    if request.method == 'POST':
        if "broadcast" in request.POST:
            temp = {
                'farmerId' : request.POST.get('farmerId'),
                'cropName' : request.POST.get('cropName'),
                'quantity' : int(request.POST.get('quantity')),
                'expectedPrice' : int(request.POST.get('expectedPrice')),
                'timestamp': datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"),
                'availableQuantity' : int(request.POST.get('quantity')),
            }
            database.child("user").child("Farmer").child('yields').child(sess).push(temp)
        if "insurance" in request.POST:
                print("insure")

                temp ={
                    'processorKey': request.POST.get('processorKey'),
                    'farmerKey': request.POST.get('farmerKey'),
                    'interestKey':request.POST.get('selfKey'),
                    'checked':0,
                }
                print('check checkedddddddddddddddddddd')
                print(temp)


                # To reduce on request to insurance
                fetchLotNumber = database.child("user").child("Processor").child("interests").child(request.POST.get('processorKey')).\
                    child(request.POST.get('selfKey')).get()
                print(fetchLotNumber)
                fetchLotNumberValue = fetchLotNumber.val()['farmerLotKey']
                print(fetchLotNumberValue)
                requestedQuantity = fetchLotNumber.val()['quantityRequested']
                toReduceInfo = database.child("user").child("Farmer").child("yields").child(sess).child(fetchLotNumberValue).get()
                toReducInfo = toReduceInfo.val()
                toReducInfo['quantity'] = int(toReducInfo['quantity']) - int(requestedQuantity)
                database.child("user").child("Farmer").child("yields").child(sess).child(fetchLotNumberValue).update(toReducInfo)


                database.child("user").child("Quality Checker").child("0zGbx6o6oiWIqqABxfy5Qxo07kh2").child("check").push(temp)

        if "statusButton" in request.POST:
            # Check if selected Lot number is correct or not



            # print(request.POST.get('idSelect'))
            # print(request.POST.get('lotIdSelect'))
            print(request.POST)
            print(request.GET['lotIdSelect'])


    data = database.child("user").child("Farmer").child('yields').child(sess).get()
    temp = []
    if data.val() is not None:
        for i in data.each():
            temp.append(i.val())
    results = []
    ordersAlreadyForInspection = []
    resultData = database.child("user").child("Quality Checker").child("0zGbx6o6oiWIqqABxfy5Qxo07kh2").child(
        "check").get()
    for check in resultData.each():
        value = check.val()
        interestKey = value['interestKey']
        ordersAlreadyForInspection.append(interestKey)
    print('heyyyyyyy')
    print(ordersAlreadyForInspection)
    resultData = database.child("user").child("Processor").child('interests').get()
    for entry in resultData.each():
        value = entry.val()
        for key, values in value.items():
            print('keyyyyyyy')
            print(key)
            if key in ordersAlreadyForInspection:
                continue
            if values['farmerKey'] == sess:
                dict = {'processorKey': entry.key()}
                dict1 = {'selfKey': key}
                # print(key)
                val = values
                val.update(dict)
                val.update(dict1)
                results.append(val)
    # print(results)
    # transaction from processor
    # transactionHistoryValues = []
    # dataForTransaction = database.child('user').child('Processor').child('Confirmed Farmer Orders').get()
    # # print(dataForTransaction.val())
    # for key,value in dataForTransaction.val().items():
    #     print(key)
    #     for val in value:
    #         print(val) 'transactionHistory':transactionHistoryValues

    getFarmerYields(sess)
    # print("results:", results)
    return render(request,'user/farmer.html',{'data':temp,'results':results})



def qualityChecker(request):
    result=[]
    checkerId = "0zGbx6o6oiWIqqABxfy5Qxo07kh2"
    if request.method == "POST":
        remark = request.POST.get('remark')
        sampleSize = request.POST.get('sampleSize')
        quantity = request.POST.get('quantity')
        defective = request.POST.get('defective')
        farmerLotKey = request.POST.get('lotKey')
        inspectorData = database.child("user").child("Quality Checker").child(checkerId).get()
        farmerKey = request.POST.get('farmerKey')
        farmerData = database.child("user").child("Farmer").child(farmerKey).get()
        sampleSize = int(sampleSize)
        quantity = int(quantity)
        defective = int(defective)
        print(sampleSize)
        interestKey = request.POST.get('interestKey')
        print(type(sampleSize))
        if "pushButton" in request.POST:
            if inspectorData is not None:
                inspectorAddress = inspectorData.val()['address']
                if farmerData is not None:
                    farmerAddress = farmerData.val()['address']
                    # tx_hash = contract.functions.addQualityReport(farmerAddress, inspectorAddress, interestKey,
                    #                                               remark,sampleSize,quantity,defective).transact()
                    # tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
                    data = database.child("user").child("Quality Checker").child(checkerId).child("check").get()
                    for dat in data.each():
                        key = dat.key()
                        val = dat.val()
                        if(val['interestKey'] == interestKey):
                            database.child("user").child("Quality Checker").child(checkerId).child("check").child(key).update({"checked": 1,
                                                                                                        "interestKey":interestKey,
                                                                                                        "farmerKey":val['farmerKey'],
                                                                                                        "processorKey":val['processorKey'],
                                                                                                                               })
                            # add data corresponding to interest key from processor -> processorKey -> interestKey
                            quantityRequested = database.child("user").child("Processor").child("interests").child(val['processorKey']).child(interestKey).get()
                            quantityFetched = int(quantityRequested.val()['quantityRequested'])
                            quotedPriceFetched = int(quantityRequested.val()['quotedPrice'])
                            information = {
                                'farmerKey': val['farmerKey'],
                                'interestKey':val['interestKey'],
                                'quantity': quantityFetched,
                                'quoted price': quotedPriceFetched,
                                'paymentStatus':0,
                                'reportStatus': 0,
                            }
                            database.child("user").child("Processor").child('Confirmed Farmer Orders').child(
                                val['processorKey']).child(interestKey).set(information)
                            # database.child("user").child("Processor").child('Confirmed Orders').child(
                            #     val['processorKey']).child(interestKey).set(infor)
            print('blockchain mein add hoga')
        else:
            print('nahi hoga')

    resultData = database.child("user").child("Quality Checker").child(checkerId).child("check").get()
    for check in resultData.each():
        value = check.val()
        if(value['checked']==1):
            continue
        interestKey = value['interestKey']
        user = database.child("user").child("Farmer").get()
        for i in user.each():
            dict1 = {}
            if (i.key() == value['farmerKey']):
                userLotCheck = database.child("user").child("Processor").child("interests").child(
                    value['processorKey']).get()
                for j in userLotCheck.each():
                    # print(j.key())
                    # print(value['interestKey'])
                    dict2 = {}
                    if (j.key() == value['interestKey']):
                        dict1 = i.val()
                        dict2 = j.val()
                        dict2.update({'interestKey':interestKey})
                        # print("1:::::::", dict1)
                        # print("2:::::::", dict2)
                        dict1.update(dict2)
                        print(dict1)
                        # print("com:::::::", dict1)
                        result.append(dict1)
    return render(request, 'user/qualityChecker.html',{'data':result})

def payments(request):
    if request.method == 'POST':
        account_1 = request.POST.get('selfAddress')
        account_2 = request.POST.get('receiverAddress')
        private_key = request.POST.get('selfPrivateKey')
        renderedFrom = request.POST.get('renderedFrom')
        amountPayable = request.POST.get('amountPayable')

        nonce = web3.eth.getTransactionCount(account_1)
        tx = {
            'nonce': nonce,
            'to': account_2,
            'value': web3.toWei(amountPayable, 'ether'),
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei'),
        }
        signed_tx = web3.eth.account.signTransaction(tx, private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(web3.toHex(tx_hash))
        if renderedFrom == 'processor':
            processorKey = request.POST.get('processorKey')
            lotNumber = request.POST.get('lotNumber')
            data = database.child("user").child("Processor").child("Confirmed Farmer Orders").child(processorKey).child(lotNumber).get()
            print(data.val())
            temp = data.val()
            temp['paymentStatus'] = 1
            database.child("user").child("Processor").child("Confirmed Farmer Orders").child(processorKey).child(
                lotNumber).update(temp)
    redirectTo = "/"+renderedFrom+"/"
    return redirect(redirectTo)

def processor(request):
    sess = request.session['uid']
    processorId = sess
    if request.method=='POST':
        if "acceptButton" in request.POST:
            data = {
                'farmerId': request.POST.get('farmerId'),
                'farmerLotKey' :request.POST.get('farmerLotKey'),
                'farmerKey': request.POST.get('farmerKey'),
                'cropName': request.POST.get('cropName'),
                'quantityRequested': request.POST.get('requiredQuantity'),
                'quotedPrice': request.POST.get('quotedPrice'),
                'quality': "N"
            }
            farmerKey = request.POST.get('farmerKey')
            farmerLotKey = request.POST.get('farmerLotKey')
            quantityRequested = int(request.POST.get('requiredQuantity'))
            availaibleQuantity = database.child('user').child('Farmer').child('yields').child(farmerKey).child(farmerLotKey).get()
            if availaibleQuantity.val()['quantity'] < quantityRequested or availaibleQuantity.val()['availableQuantity'] < quantityRequested:
                return redirect('/processor/')
            updateDetails = availaibleQuantity.val()
            updateDetails['availableQuantity'] = updateDetails['availableQuantity'] - quantityRequested
            database.child('user').child('Farmer').child('yields').child(farmerKey).child(farmerLotKey).update(updateDetails)
            database.child("user").child("Processor").child('interests').child(processorId).push(data)
        if "paymentFarmerButton" in request.POST:
            amountPayable = request.POST['amountPayable']
            lotNumber = request.POST['lotNumber']
            return render(request,"user/payment.html",{'renderedFrom':'processor','amountPayable':amountPayable,'lotNumber':lotNumber,
                                                       'processorKey':sess})
        if "reportAddButton" in request.POST:
            farmerAddress = request.POST.get('farmerAddress')
            processorAddress = request.POST.get('processorAddress')
            lotNumber = request.POST.get('lotNumber')
            processorRemarksOnPurchasedProducts = request.POST.get('processorRemarksOnPurchasedProducts')
            receivedShipments = request.POST.get('receivedShipments')
            # tx_hash = contract.functions.addProcessorReport(processorAddress,farmerAddress, lotNumber,processorRemarksOnPurchasedProducts,receivedShipments).transact()
            # tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            reportTransactionsUpdateData = database.child("user").child("Processor").child(
                "Confirmed Farmer Orders").child(sess).child(lotNumber).get()
            reportTransactionData = reportTransactionsUpdateData.val()
            reportTransactionData['reportStatus'] = 1
            #print(reportTransactionData)
            reportTransactionsUpdateData = database.child("user").child("Processor").child(
                "Confirmed Farmer Orders").child(sess).child(lotNumber).update(reportTransactionData)
    data = database.child("user").child("Farmer").child('yields').get()
    temp = []
    reportPaidTransactions = []
    pendingFarmerTransactions = []
    #print(sess)
    dataForFarmerTransactions = database.child("user").child("Processor").child("Confirmed Farmer Orders").child(sess).get()
    for transaction in dataForFarmerTransactions.each():
        transactionKey = transaction.key()
        transactionValue = transaction.val()
        print(transactionValue)
        # print(transactionValue)

        # print(transactionValue['paymentStatus'])
        amountPayable = transactionValue['quantity']*transactionValue['quoted price']
        temporaryData = {
            'farmerKey':transactionValue['farmerKey'],
            'lotNumber': transactionValue['interestKey'],
            'quantity': transactionValue['quantity'],
            'quotedPrice' : transactionValue['quoted price'],
            'amountPayable':amountPayable
        }
        if transactionValue['reportStatus'] == 0 and transactionValue['paymentStatus'] == 1:
            farmerData = database.child("user").child("Farmer").child(transactionValue['farmerKey']).get()
            processorData = database.child("user").child("Processor").child(sess).get()
            reportData = {
                'farmerAddress':farmerData.val()['address'],
                'processorAddress':processorData.val()['address']
            }
            reportData.update(temporaryData)
            reportPaidTransactions.append(reportData)
            # print(reportData)
        if transactionValue['paymentStatus'] == 1:
            continue
        pendingFarmerTransactions.append(temporaryData)
    for entry in data.each():
        dict = {'farmerKey': entry.key()}
        hey = entry.val()
        for key, values in hey.items():
            val = values
            dict1 = {'farmerLotKey': key}
            #print(val)
            val.update(dict)
            val.update(dict1)
            #print(val)
            if(val['quantity']>0 and val['availableQuantity']>0):
                temp.append(val)
    # Transaction History Orders Data
    transactionHistoryValues = []
    dataForTransaction = database.child('user').child('Processor').child('Confirmed Farmer Orders').child(sess).get()
    for transactions in dataForTransaction.each():
        tempTransact = transactions.val()
        tempTransact.update({'confirmedKey':transactions.key()})
        if (tempTransact['paymentStatus'] == 1 and tempTransact['reportStatus'] == 1):
            transactionHistoryValues.append(tempTransact)

            print("-------------------------------------",transactionHistoryValues)
    data = database.child("user").child("Processor").child("Confirmed Farmer Orders").child(processorId).get()
    
    lots =[]
    for lotKey in data.each():
        lots.append(lotKey.key())
    #print(lots)
    if request.method == "POST":
        if "broadcast" in request.POST:
            product = {
                'lotKey': request.POST['dropdown'],
                'productName': request.POST.get('productName'),
                'quantity': int(request.POST.get('quantity')),
                'Price': int(request.POST.get('Price')),
                'timestamp': datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"),
                'availableQuantity' : int(request.POST.get('quantity'))
            }
            database.child("user").child("Processor").child('products').child(processorId).push(product)

    # display orders done with retailer
    temp1=database.child("user").child("Retailer").child('Confirmed Processor Orders').get()
    RorderDetails=[]

    for ret in temp1.each():
        
        for key, item in ret.val().items():
            if key==processorId:
            
                for key,item1 in item.items():
                    dict1={'processorKey':key}
                    dict1.update(item1)
                    RorderDetails.append(dict1)
    #print("-------------------------------------",transactionHistoryValues)
    return render(request, 'user/processor.html',{'data':temp,'farmerPaymentData':pendingFarmerTransactions,'reportPaidTransactions':reportPaidTransactions,'transactionHistory':transactionHistoryValues,'lots':lots,'orderDetails':RorderDetails})
def signIn(request):
    # if method == 'POST':

    return render(request, 'user/signIn.html')


def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = auth.sign_in_with_email_and_password(email, passw)
        session_id = user['localId']
        request.session['uid'] = str(session_id)
        # print(user)
        stake = request.POST['drop']
        users = database.child("user").child(stake).get()

        for u in users.each():
            if u.key() == session_id:
                context = u.val()
        if stake == "Farmer":
            return redirect("/farmer/")
        if stake == "Customer":
            return redirect("/customer/")
        if stake == "Logistics":
            return redirect("/logistics/")
        if stake == "Retailer":
            return redirect("/retailer/")
        if stake == "Processor":
            return redirect("/processor/")
        if stake == "Quality Checker":
            return redirect("/qualityChecker/")
    except:
        message = "Invalid credentials"
        return render(request, "user/signIn.html", {"msg": message})

    session_id = user['localId']
    request.session['uid'] = str(session_id)
    # print(user)
    stake = request.POST['drop']

    users = database.child("user").child(stake).get()

    for u in users.each():
        if u.key() == session_id:
            context = u.val()
    if stake == "Farmer":
        return redirect("/farmer/")
    if stake == "Customer":
        return redirect("/customer/")
    if stake == "Logistics":
        return redirect("/logistics/")
    if stake == "Retailer":
        return redirect("/retailer/")
    if stake == "Processor":
        return redirect("/processor/")
    if stake == "Quality Checker":
        return redirect("/qualityChecker/")




def signUp(request):
    return render(request, 'user/signup.html')

def postsignUp(request):
    name=request.POST.get('name')
    email=request.POST.get('email')
    passw = request.POST.get('pass')
    stake = request.POST['drop']
    address = request.POST['address']
    user = auth.create_user_with_email_and_password(email,passw)
    print(stake)
    print(email)
    id=user['localId']
    data={
        'name':name,
        'email':email,
        'address':address
    }

    database.child("user").child(stake).child(id).set(data)
    return render(request,"user/signIn.html")


def retailer(request):
    productDetails = []
    retailerId = request.session['uid']

    if request.method == "POST":
        if "accept" in request.POST:
            checkData = database.child("user").child("Processor").child('products').child(
                request.POST.get('processorKey')).child(request.POST.get('productKey')).get()
            print('fghjkhgkhlkhlkjhlkjhlkjhhkkjkbknm')
            print(checkData.val()['availableQuantity'])
            if checkData.val()['availableQuantity'] < int(request.POST.get('requiredQuantity')):
                print("inside if ")
                return redirect('/retailer/')
            transaction = {
                # 'lotKey': request.POST.get('lotKey'),
                'productName': request.POST.get('productName'),
                'requiredQuantity': int(request.POST.get('requiredQuantity')),
                'Price': int(request.POST.get('Price')),
                'timestamp': datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"),
                'processorKey': request.POST.get('processorKey'),
                'productKey': request.POST.get('productKey'),
                'reportAdded': 0,
                'lotKey': request.POST.get('lotKey')
            }
            processorKey = request.POST.get('processorKey')
            database.child("user").child("Retailer").child('Confirmed Processor Orders').child(retailerId).push(
                transaction)

            # change the available quantity

            requiredQuantity = int(transaction['requiredQuantity'])
            processorKey = transaction['processorKey']
            productKey = transaction['productKey']
            temp = database.child("user").child("Processor").child("products").child(processorKey).child(
                productKey).get()

            values = temp.val()
            avqty = int(values['availableQuantity'])
            avqty = avqty - requiredQuantity
            print(avqty)

            database.child("user").child("Processor").child("products").child(processorKey).child(productKey).update(
                {"availableQuantity": avqty})
    data = database.child("user").child("Processor").child('products').get()
    for entry in data.each():
        processor = {'processorKey': entry.key()}
        product = entry.val()

        for key, value in product.items():
            dict = {"productKey": key}
            details = value
            details.update(dict)
            details.update(processor)
            if value['availableQuantity'] <= 0:
                continue
            productDetails.append(details)
    print(productDetails)

    # display confirmed orders
    temp = database.child("user").child("Retailer").child('Confirmed Processor Orders').child(retailerId).get()
    orderDetails = []
    for x in temp.each():
        z = x.val()

        orderDetails.append(z)

     # Broadcast for retailer
    processorKeys = []
    transactionDetails = []
    data = database.child("user").child("Retailer").child("Confirmed Processor Orders").child(retailerId).get()
    details = {}
    retailerKey = {'retailerKey' : retailerId}
    for entry in data.each():
        processorKey = {'processorKey': entry.key()}
        processorKeys.append(entry.key())
        product = entry.val()
        print(product)
        print("23r768trqwd6tet1tw3etqt12yityiet12378t")
        for key in product.keys():
            transactionKeys = {'transactionKey' : key}
            details.update(transactionKeys)
            details.update(processorKey)
            details.update(product[key])
            details.update(retailerKey)
            transactionDetails.append(details)
    print("--------------------------")
    print(transactionDetails)
    print("--------------------------")
    if request.method == "POST":
        if "broadcast" in request.POST:
            transactionKey = request.POST['dropdown2']
            data = database.child("user").child("Retailer").child("Confirmed Processor Orders").child(retailerId).child(request.POST['dropdown1']).child(transactionKey).get()
            item = {
                'processorKey': request.POST['dropdown1'],
                'transactionKey': request.POST['dropdown2'],
                'totalQuantity': int(request.POST.get('quantity')),
                'Price': int(request.POST.get('Price')),
                'timestamp': datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"),
                'availableQuantity': int(request.POST.get('quantity')),
                'productName' : data.val()['productName']
            }
            database.child("user").child("Retailer").child('products').child(retailerId).push(item)

    return render(request , 'user/retailer.html' ,
                  {'data' : productDetails, 'orderDetails':orderDetails ,
                    'transactionDetails' : transactionDetails , 'processorKeys': processorKeys})


def customer(request):
    customerId = request.session['uid']
    # data = database.child("user").child("Retailer").child("Confirmed Processor Orders").get()
    data = database.child("user").child("Retailer").child("products").get()
    print(data.val())
    print("------------------------------------")
    productList = []
    details = {}
    for retailerKeys , value in data.val().items():
        retailerKey = {'retailerKey' : retailerKeys}
        for transactionKey , transactionsData in value.items():
            transactionKeys = {'transactionKey' : transactionKey}
            details.update(transactionsData)
            details.update(transactionKeys)
            details.update(retailerKey)
            productList.append(details)
    print(productList)
    return render(request , 'user/customer.html' ,{'productList' : productList} )    


def logout(request):
    authe.logout(request)
    return render(request, 'user/signIn.html')

def home(request):
    return render(request,'user/home.html')

def getFarmerYields(farmerId,detailed = 0):
    data = database.child('user').child('Farmer').child('yields').child(farmerId).get()
    print('Inside Function')
    yieldIds = []
    for dat in data.each():
        yieldIds.append(dat.key())

    return yieldIds

def getData(request):
    sess = request.session['uid']
    post_id = request.GET.get('requestData')

    if post_id == 'yieldIds':
        yieldIds = getFarmerYields(sess)
        dataToBeTransferred = []
        for i in range(len(yieldIds)):
            temp = {'yieldIds':yieldIds[i]}
            dataToBeTransferred.append(temp)
        print(sess)
        print(dataToBeTransferred)
        return JsonResponse(dataToBeTransferred,safe=False)
    elif post_id == 'lotIds':
        print('else ma che')
        selectedItem = request.GET.get('selectedItem')
        checkerId = "0zGbx6o6oiWIqqABxfy5Qxo07kh2"
        resultData = database.child("user").child("Quality Checker").child(checkerId).child("check").get()
        dataToBeTransferred = []
        for check in resultData.each():
            value = check.val()
            if value['farmerKey'] != sess:
                continue
            interestKey = value['interestKey']
            processorKey = value['processorKey']
            fetchLotFromProcessorInterests = database.child("user").child("Processor").child('interests').child(processorKey).child(interestKey).get()
            if fetchLotFromProcessorInterests.val()['farmerLotKey'] == selectedItem:
                dataToBeTransferred.append({'lotNumbers':interestKey})
        print(dataToBeTransferred)
        return JsonResponse(dataToBeTransferred,safe=False)