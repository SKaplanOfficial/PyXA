from time import sleep
from typing import Any, List
from aem import Application
from click import command
import objc
import CoreServices
import ApplicationServices
import struct

import objc
from AppKit import NSURL, NSApp, NSData
import AppKit
import Quartz

from Foundation import NSBundle

def send_save_event(pid: str):
    s_down = Quartz.CGEventCreateKeyboardEvent(None, 1, True)
    s_up = Quartz.CGEventCreateKeyboardEvent(None, 1, False)
    shift_down = Quartz.CGEventCreateKeyboardEvent(None, 56, True)
    shift_up = Quartz.CGEventCreateKeyboardEvent(None, 56, False)
    command_down = Quartz.CGEventCreateKeyboardEvent(None, 55, True)
    command_up = Quartz.CGEventCreateKeyboardEvent(None, 55, False)

    Quartz.CGEventPostToPid(pid, shift_down)
    Quartz.CGEventPostToPid(pid, s_down)
    Quartz.CGEventPostToPid(pid, s_up)
    Quartz.CGEventPostToPid(pid, s_down)
    Quartz.CGEventPostToPid(pid, s_up)
    Quartz.CGEventPostToPid(pid, shift_up)

    # print(s_down)
    # Quartz.CGEventPost(Quartz.kCGHIDEventTap, s_down)
    # Quartz.CGEventPost(Quartz.kCGHIDEventTap, command_down)

def send_copy_event(pid: str):
    c_down = Quartz.CGEventCreateKeyboardEvent(objc.NULL, 8, True)
    c_up = Quartz.CGEventCreateKeyboardEvent(objc.NULL, 8, False)
    command_down = Quartz.CGEventCreateKeyboardEvent(objc.NULL, 55, True)
    command_up = Quartz.CGEventCreateKeyboardEvent(objc.NULL, 55, False)

    Quartz.CGEventPostToPid(pid, c_down)
    Quartz.CGEventPostToPid(pid, command_down)
    Quartz.CGEventPostToPid(pid, c_up)
    Quartz.CGEventPostToPid(pid, command_up)

def OSType(s):
    return int.from_bytes(s.encode("UTF-8"), "big")

event_manager = ApplicationServices.NSAppleEventManager.sharedAppleEventManager()

def send_event_to_bundle(event_type: int, event: int, bundle: str):
    app_desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeApplicationBundleID, bundle.encode("UTF-8"))

    new_event = ApplicationServices.NSAppleEventDescriptor.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_(event_type, event, app_desc, kAutoGenerateReturnID, kAnyTransactionID)

    new_event.sendEventWithOptions_timeout_error_(kAEWaitReply|kAECanInteract, kAEDefaultTimeout, None)

def test():
    bundle = "com.apple.TextEdit"
    app_desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeApplicationBundleID, bundle.encode("UTF-8"))

    # event = ApplicationServices.NSAppleEventDescriptor.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_(kCoreEventClass, event, app_desc, kAutoGenerateReturnID, kAnyTransactionID)

    # file_desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeFileURL, "/".encode("UTF-8"))
    # event.setParamDescriptor_forKeyword_(file_desc, kAERevealSelection)

    #fileList = ApplicationServices.NSAppleEventDescriptor.listDescriptor()
    createEvent = ApplicationServices.NSAppleEventDescriptor.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_(kAECoreSuite, kAECreateElement, app_desc, kAutoGenerateReturnID, kAnyTransactionID)

    url = NSURL.alloc().initFileURLWithPath_("/Users/steven/Documents/blah.txt")
    desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(cDocument, url.absoluteString().encode("UTF-8"))
    #fileList.insertDescriptor_atIndex_(desc, 0)

    createEvent.setParamDescriptor_forKeyword_(desc, keyAEObjectClass)
    createEvent.sendEventWithOptions_timeout_error_(kAEWaitReply|kAECanInteract, kAEDefaultTimeout, None)

kAENoReply            =  1
kAENeverInteract      = 16
kAEDefaultTimeout     = -1
kAnyTransactionID     =  0
kAutoGenerateReturnID = -1

kAECanInteract        = 0x00000020
kAEWaitReply          = 0x00000003

typeAEList                    = OSType('list')
typeAERecord                  = OSType('reco')
typeEventRecord               = OSType('evrc')
typeAppleEvent                = OSType('aevt')
typeApplicationBundleID       = OSType('bund')
typeApplSignature             = OSType('sign')
typeFSRef                     = OSType('fsrf')
typeFileURL                   = OSType('furl')
typeApplicationURL            = OSType('aprl')
typeAppParameters             = OSType('appa')
typeTrue                      = OSType('true')
typeFalse                     = OSType('fals')
typeKernelProcessID           = OSType('kpid')
typeProcessSerialNumber       = OSType('psn ')
typeFixed                     = OSType('fixd')
typeBookmarkData              = OSType('bmrk')
typeWildCard                  = OSType('****')
typeKeyword                   = OSType('keyw')

kAEOpenApplication            = OSType('oapp')
kAEOpenDocuments              = OSType('odoc')
kAEPrintDocuments             = OSType('pdoc')
kAEOpenContents               = OSType('ocon')
kAEQuitApplication            = OSType('quit')
kAEAnswer                     = OSType('ansr')
kAEApplicationDied            = OSType('obit')
kAEShowPreferences            = OSType('pref')

keyDirectObject = OSType('----')

def xaevent_quit_application_by_bundle_id(bundle_id: str):
    send_event_to_bundle(kAEQuitApplication, "com.apple.MobileSMS")

cAEList                       = OSType('list')
cApplication                  = OSType('capp')
cArc                          = OSType('carc')
cBoolean                      = OSType('bool')
cCell                         = OSType('ccel')
cChar                         = OSType('cha ')
cColorTable                   = OSType('clrt')
cColumn                       = OSType('ccol')
cDocument                     = OSType('docu')
cDrawingArea                  = OSType('cdrw')
cEnumeration                  = OSType('enum')
cFile                         = OSType('file')
cFixed                        = OSType('fixd')
cFixedPoint                   = OSType('fpnt')
cFixedRectangle               = OSType('frct')
cGraphicLine                  = OSType('glin')
cGraphicObject                = OSType('cgob')
cGraphicShape                 = OSType('cgsh')
cGraphicText                  = OSType('cgtx')
cGroupedGraphic               = OSType('cpic')

cInsertionLoc                 = OSType('insl')
cInsertionPoint               = OSType('cins')
cIntlText                     = OSType('itxt')
cIntlWritingCode              = OSType('intl')
cItem                         = OSType('citm')
cLine                         = OSType('clin')
cLongDateTime                 = OSType('ldt ')
cLongFixed                    = OSType('lfxd')
cLongFixedPoint               = OSType('lfpt')
cLongFixedRectangle           = OSType('lfrc')
cLongInteger                  = OSType('long')
cLongPoint                    = OSType('lpnt')
cLongRectangle                = OSType('lrct')
cMachineLoc                   = OSType('mLoc')
cMenu                         = OSType('cmnu')
cMenuItem                     = OSType('cmen')
cObject                       = OSType('cobj')
cObjectSpecifier              = OSType('obj ')
cOpenableObject               = OSType('coob')
cOval                         = OSType('covl')

cParagraph                    = OSType('cpar')
cPICT                         = OSType('PICT')
cPixel                        = OSType('cpxl')
cPixelMap                     = OSType('cpix')
cPolygon                      = OSType('cpgn')
cProperty                     = OSType('prop')
cQDPoint                      = OSType('QDpt')
cQDRectangle                  = OSType('qdrt')
cRectangle                    = OSType('crec')
cRGBColor                     = OSType('cRGB')
cRotation                     = OSType('trot')
cRoundedRectangle             = OSType('crrc')
cRow                          = OSType('crow')
cSelection                    = OSType('csel')
cShortInteger                 = OSType('shor')
cTable                        = OSType('ctbl')
cText                         = OSType('ctxt')
cTextFlow                     = OSType('cflo')
cTextStyles                   = OSType('tsty')
cType                         = OSType('type')

cVersion                      = OSType('vers')
cWindow                       = OSType('cwin')
cWord                         = OSType('cwor')
enumArrows                    = OSType('arro')
enumJustification             = OSType('just')
enumKeyForm                   = OSType('kfrm')
enumPosition                  = OSType('posi')
enumProtection                = OSType('prtn')
enumQuality                   = OSType('qual')
enumSaveOptions               = OSType('savo')
enumStyle                     = OSType('styl')
enumTransferMode              = OSType('tran')
kAEAbout                      = OSType('abou')
kAEAfter                      = OSType('afte')
kAEAliasSelection             = OSType('sali')
kAEAllCaps                    = OSType('alcp')
kAEArrowAtEnd                 = OSType('aren')
kAEArrowAtStart               = OSType('arst')
kAEArrowBothEnds              = OSType('arbo')

kAEAsk                        = OSType('ask ')
kAEBefore                     = OSType('befo')
kAEBeginning                  = OSType('bgng')
kAEBeginsWith                 = OSType('bgwt')
kAEBeginTransaction           = OSType('begi')
kAEBold                       = OSType('bold')
kAECaseSensEquals             = OSType('cseq')
kAECentered                   = OSType('cent')
kAEChangeView                 = OSType('view')
kAEClone                      = OSType('clon')
kAEClose                      = OSType('clos')
kAECondensed                  = OSType('cond')
kAEContains                   = OSType('cont')
kAECopy                       = OSType('copy')
kAECoreSuite                  = OSType('core')
kAECountElements              = OSType('cnte')
kAECreateElement              = OSType('crel')
kAECreatePublisher            = OSType('cpub')
kAECut                        = OSType('cut ')
kAEDelete                     = OSType('delo')

kAEDoObjectsExist             = OSType('doex')
kAEDoScript                   = OSType('dosc')
kAEDrag                       = OSType('drag')
kAEDuplicateSelection         = OSType('sdup')
kAEEditGraphic                = OSType('edit')
kAEEmptyTrash                 = OSType('empt')
kAEEnd                        = OSType('end ')
kAEEndsWith                   = OSType('ends')
kAEEndTransaction             = OSType('endt')
kAEEquals                     = OSType('=   ')
kAEExpanded                   = OSType('pexp')
kAEFast                       = OSType('fast')
kAEFinderEvents               = OSType('FNDR')
kAEFormulaProtect             = OSType('fpro')
kAEFullyJustified             = OSType('full')
kAEGetClassInfo               = OSType('qobj')
kAEGetData                    = OSType('getd')
kAEGetDataSize                = OSType('dsiz')
kAEGetEventInfo               = OSType('gtei')
kAEGetInfoSelection           = OSType('sinf')

kAEGetPrivilegeSelection      = OSType('sprv')
kAEGetSuiteInfo               = OSType('gtsi')
kAEGreaterThan                = OSType('>   ')
kAEGreaterThanEquals          = OSType('>=  ')
kAEGrow                       = OSType('grow')
kAEHidden                     = OSType('hidn')
kAEHiQuality                  = OSType('hiqu')
kAEImageGraphic               = OSType('imgr')
kAEIsUniform                  = OSType('isun')
kAEItalic                     = OSType('ital')
kAELeftJustified              = OSType('left')
kAELessThan                   = OSType('<   ')
kAELessThanEquals             = OSType('<=  ')
kAELowercase                  = OSType('lowc')
kAEMakeObjectsVisible         = OSType('mvis')
kAEMiscStandards              = OSType('misc')
kAEModifiable                 = OSType('modf')
kAEMove                       = OSType('move')
kAENo                         = OSType('no  ')
kAENoArrow                    = OSType('arno')

# kAENonmodifiable
kAENonmodifiable              = OSType('nmod')
kAEOpen                       = OSType('odoc')
kAEOpenSelection              = OSType('sope')
kAEOutline                    = OSType('outl')
kAEPageSetup                  = OSType('pgsu')
kAEPaste                      = OSType('past')
kAEPlain                      = OSType('plan')
kAEPrint                      = OSType('pdoc')
kAEPrintSelection             = OSType('spri')
kAEPrintWindow                = OSType('pwin')
kAEPutAwaySelection           = OSType('sput')
kAEQDAddOver                  = OSType('addo')
kAEQDAddPin                   = OSType('addp')
kAEQDAdMax                    = OSType('admx')
kAEQDAdMin                    = OSType('admn')
kAEQDBic                      = OSType('bic ')
kAEQDBlend                    = OSType('blnd')
kAEQDCopy                     = OSType('cpy ')
kAEQDNotBic                   = OSType('nbic')
kAEQDNotCopy                  = OSType('ncpy')

# kAEQDNotOr
kAEQDNotOr                    = OSType('ntor')
kAEQDNotXor                   = OSType('nxor')
kAEQDOr                       = OSType('or  ')
kAEQDSubOver                  = OSType('subo')
kAEQDSubPin                   = OSType('subp')
kAEQDSupplementalSuite        = OSType('qdsp')
kAEQDXor                      = OSType('xor ')
kAEQuickdrawSuite             = OSType('qdrw')
kAEQuitAll                    = OSType('quia')
kAERedo                       = OSType('redo')
kAERegular                    = OSType('regl')
kAEReopenApplication          = OSType('rapp')
kAEReplace                    = OSType('rplc')
kAERequiredSuite              = OSType('reqd')
kAERevealSelection            = OSType('srev')
kAERevert                     = OSType('rvrt')
kAERightJustified             = OSType('rght')
kAESave                       = OSType('save')
kAESelect                     = OSType('slct')
kAESetData                    = OSType('setd')

# kAESetPosition
kAESetPosition                = OSType('posn')
kAEShadow                     = OSType('shad')
kAEShowClipboard              = OSType('shcl')
kAESmallCaps                  = OSType('smcp')
kAESpecialClassProperties     = OSType('c@#!')
kAEStrikethrough              = OSType('strk')
kAESubscript                  = OSType('sbsc')
kAESuperscript                = OSType('spsc')
kAETableSuite                 = OSType('tbls')
kAETextSuite                  = OSType('TEXT')
kAETransactionTerminated      = OSType('ttrm')
kAEUnderline                  = OSType('undl')
kAEUndo                       = OSType('undo')
kAEWholeWordEquals            = OSType('wweq')
kAEYes                        = OSType('yes ')
kAEZoom                       = OSType('zoom')

# kAELogOut
kAESleep                      = OSType('slep')
kAELogOut                     = OSType('logo')
kAEReallyLogOut               = OSType('rlgo')
kAEShutDown                   = OSType('shut')
kAEShowRestartDialog          = OSType('rrst')
kAEShowShutdownDialog         = OSType('rsdn')
kAERestart                    = OSType('rest')

def xaevent_sleep():
    send_event_to_bundle(kAESleep, "com.apple.loginwindow")

def xaevent_show_logout_dialog():
    send_event_to_bundle(kAELogOut, "com.apple.loginwindow")

def xaevent_logout_immediately():
    send_event_to_bundle(kAEReallyLogOut, "com.apple.loginwindow")

def xaevent_show_restart_dialog():
    send_event_to_bundle(kAEShowRestartDialog, "com.apple.loginwindow")

def xaevent_restart_immediately():
    send_event_to_bundle(kAERestart, "com.apple.loginwindow")

def xaevent_show_shutdown_dialog():
    send_event_to_bundle(kAEShowShutdownDialog, "com.apple.loginwindow")

def xaevent_shutdown_immediately():
    send_event_to_bundle(kAEShutDown, "com.apple.loginwindow")

# kAEMouseClass
kAEMouseClass                 = OSType('mous')
kAEDown                       = OSType('down')
kAEUp                         = OSType('up  ')
kAEMoved                      = OSType('move')
kAEStoppedMoving              = OSType('stop')
kAEWindowClass                = OSType('wind')
kAEUpdate                     = OSType('updt')
kAEActivate                   = OSType('actv')
kAEDeactivate                 = OSType('dact')
kAECommandClass               = OSType('cmnd')
kAEKeyClass                   = OSType('keyc')
kAERawKey                     = OSType('rkey')
kAEVirtualKey                 = OSType('keyc')
kAENavigationKey              = OSType('nave')
kAEAutoDown                   = OSType('auto')
kAEApplicationClass           = OSType('appl')
kAESuspend                    = OSType('susp')
kAEResume                     = OSType('rsme')
kAEDiskEvent                  = OSType('disk')
kAENullEvent                  = OSType('null')
kAEWakeUpEvent                = OSType('wake')
kAEScrapEvent                 = OSType('scrp')
kAEHighLevel                  = OSType('high')

keyAEAngle                    = OSType('kang')
keyAEArcAngle                 = OSType('parc')

keyAEBaseAddr                 = OSType('badd')
keyAEBestType                 = OSType('pbst')
keyAEBgndColor                = OSType('kbcl')
keyAEBgndPattern              = OSType('kbpt')
keyAEBounds                   = OSType('pbnd')
keyAECellList                 = OSType('kclt')
keyAEClassID                  = OSType('clID')
keyAEColor                    = OSType('colr')
keyAEColorTable               = OSType('cltb')
keyAECurveHeight              = OSType('kchd')
keyAECurveWidth               = OSType('kcwd')
keyAEDashStyle                = OSType('pdst')
keyAEData                     = OSType('data')
keyAEDefaultType              = OSType('deft')
keyAEDefinitionRect           = OSType('pdrt')
keyAEDescType                 = OSType('dstp')
keyAEDestination              = OSType('dest')
keyAEDoAntiAlias              = OSType('anta')
keyAEDoDithered               = OSType('gdit')
keyAEDoRotate                 = OSType('kdrt')

keyAEDoScale                  = OSType('ksca')
keyAEDoTranslate              = OSType('ktra')
keyAEEditionFileLoc           = OSType('eloc')
keyAEElements                 = OSType('elms')
keyAEEndPoint                 = OSType('pend')
keyAEEventClass               = OSType('evcl')
keyAEEventID                  = OSType('evti')
keyAEFile                     = OSType('kfil')
keyAEFileType                 = OSType('fltp')
keyAEFillColor                = OSType('flcl')
keyAEFillPattern              = OSType('flpt')
keyAEFlipHorizontal           = OSType('kfho')
keyAEFlipVertical             = OSType('kfvt')
keyAEFont                     = OSType('font')
keyAEFormula                  = OSType('pfor')
keyAEGraphicObjects           = OSType('gobs')
keyAEID                       = OSType('ID  ')
keyAEImageQuality             = OSType('gqua')
keyAEInsertHere               = OSType('insh')
keyAEKeyForms                 = OSType('keyf')

keyAEKeyword                  = OSType('kywd')
keyAELevel                    = OSType('levl')
keyAELineArrow                = OSType('arro')
keyAEName                     = OSType('pnam')
keyAENewElementLoc            = OSType('pnel')
keyAEObject                   = OSType('kobj')
keyAEObjectClass              = OSType('kocl')
keyAEOffStyles                = OSType('ofst')
keyAEOnStyles                 = OSType('onst')
keyAEParameters               = OSType('prms')
keyAEParamFlags               = OSType('pmfg')
keyAEPenColor                 = OSType('ppcl')
keyAEPenPattern               = OSType('pppa')
keyAEPenWidth                 = OSType('ppwd')
keyAEPixelDepth               = OSType('pdpt')
keyAEPixMapMinus              = OSType('kpmm')
keyAEPMTable                  = OSType('kpmt')
keyAEPointList                = OSType('ptlt')
keyAEPointSize                = OSType('ptsz')
keyAEPosition                 = OSType('kpos')

keyAEPropData                 = OSType('prdt')
keyAEProperties               = OSType('qpro')
keyAEProperty                 = OSType('kprp')
keyAEPropFlags                = OSType('prfg')
keyAEPropID                   = OSType('prop')
keyAEProtection               = OSType('ppro')
keyAERenderAs                 = OSType('kren')
keyAERequestedType            = OSType('rtyp')
keyAEResult                   = OSType('----')
keyAEResultInfo               = OSType('rsin')
keyAERotation                 = OSType('prot')
keyAERotPoint                 = OSType('krtp')
keyAERowList                  = OSType('krls')
keyAESaveOptions              = OSType('savo')
keyAEScale                    = OSType('pscl')
keyAEScriptTag                = OSType('psct')
keyAESearchText               = OSType('stxt')
keyAEShowWhere                = OSType('show')
keyAEStartAngle               = OSType('pang')
keyAEStartPoint               = OSType('pstp')
keyAEStyles                   = OSType('ksty')

keyAESuiteID                  = OSType('suit')
keyAEText                     = OSType('ktxt')
keyAETextColor                = OSType('ptxc')
keyAETextFont                 = OSType('ptxf')
keyAETextPointSize            = OSType('ptps')
keyAETextStyles               = OSType('txst')
keyAETextLineHeight           = OSType('ktlh')
keyAETextLineAscent           = OSType('ktas')
keyAETheText                  = OSType('thtx')
keyAETransferMode             = OSType('pptm')
keyAETranslation              = OSType('ptrs')
keyAETryAsStructGraf          = OSType('toog')
keyAEUniformStyles            = OSType('ustl')
keyAEUpdateOn                 = OSType('pupd')
keyAEUserTerm                 = OSType('utrm')
keyAEWindow                   = OSType('wndw')
keyAEWritingCode              = OSType('wrcd')

keyMiscellaneous              = OSType('fmsc')
keySelection                  = OSType('fsel')
keyWindow                     = OSType('kwnd')
keyWhen                       = OSType('when')
keyWhere                      = OSType('wher')
keyModifiers                  = OSType('mods')
keyKey                        = OSType('key ')
keyKeyCode                    = OSType('code')
keyKeyboard                   = OSType('keyb')
keyDriveNumber                = OSType('drv#')
keyErrorCode                  = OSType('err#')
keyHighLevelClass             = OSType('hcls')
keyHighLevelID                = OSType('hid ')

pArcAngle                     = OSType('parc')
pBackgroundColor              = OSType('pbcl')
pBackgroundPattern            = OSType('pbpt')
pBestType                     = OSType('pbst')
pBounds                       = OSType('pbnd')
pClass                        = OSType('pcls')
pClipboard                    = OSType('pcli')
pColor                        = OSType('colr')
pColorTable                   = OSType('cltb')
pContents                     = OSType('pcnt')
pCornerCurveHeight            = OSType('pchd')
pCornerCurveWidth             = OSType('pcwd')
pDashStyle                    = OSType('pdst')
pDefaultType                  = OSType('deft')
pDefinitionRect               = OSType('pdrt')
pEnabled                      = OSType('enbl')
pEndPoint                     = OSType('pend')
pFillColor                    = OSType('flcl')
pFillPattern                  = OSType('flpt')
pFont                         = OSType('font')

pFormula                      = OSType('pfor')
pGraphicObjects               = OSType('gobs')
pHasCloseBox                  = OSType('hclb')
pHasTitleBar                  = OSType('ptit')
pID                           = OSType('ID  ')
pIndex                        = OSType('pidx')
pInsertionLoc                 = OSType('pins')
pIsFloating                   = OSType('isfl')
pIsFrontProcess               = OSType('pisf')
pIsModal                      = OSType('pmod')
pIsModified                   = OSType('imod')
pIsResizable                  = OSType('prsz')
pIsStationeryPad              = OSType('pspd')
pIsZoomable                   = OSType('iszm')
pIsZoomed                     = OSType('pzum')
pItemNumber                   = OSType('itmn')
pJustification                = OSType('pjst')
pLineArrow                    = OSType('arro')
pMenuID                       = OSType('mnid')
pName                         = OSType('pnam')

pNewElementLoc                = OSType('pnel')
pPenColor                     = OSType('ppcl')
pPenPattern                   = OSType('pppa')
pPenWidth                     = OSType('ppwd')
pPixelDepth                   = OSType('pdpt')
pPointList                    = OSType('ptlt')
pPointSize                    = OSType('ptsz')
pProtection                   = OSType('ppro')
pRotation                     = OSType('prot')
pScale                        = OSType('pscl')
pScript                       = OSType('scpt')
pScriptTag                    = OSType('psct')
pSelected                     = OSType('selc')
pSelection                    = OSType('sele')
pStartAngle                   = OSType('pang')
pStartPoint                   = OSType('pstp')
pTextColor                    = OSType('ptxc')
pTextFont                     = OSType('ptxf')
pTextItemDelimiters           = OSType('txdl')
pTextPointSize                = OSType('ptps')

pTextStyles                   = OSType('txst')
pTransferMode                 = OSType('pptm')
pTranslation                  = OSType('ptrs')
pUniformStyles                = OSType('ustl')
pUpdateOn                     = OSType('pupd')
pUserSelection                = OSType('pusl')
pVersion                      = OSType('vers')
pVisible                      = OSType('pvis')

typeAEText                    = OSType('tTXT')
typeArc                       = OSType('carc')
typeBest                      = OSType('best')
typeCell                      = OSType('ccel')
typeClassInfo                 = OSType('gcli')
typeColorTable                = OSType('clrt')
typeColumn                    = OSType('ccol')
typeDashStyle                 = OSType('tdas')
typeData                      = OSType('tdta')
typeDrawingArea               = OSType('cdrw')
typeElemInfo                  = OSType('elin')
typeEnumeration               = OSType('enum')
typeEPS                       = OSType('EPS ')
typeEventInfo                 = OSType('evin')

typeFinderWindow              = OSType('fwin')
typeFixedPoint                = OSType('fpnt')
typeFixedRectangle            = OSType('frct')
typeGraphicLine               = OSType('glin')
typeGraphicText               = OSType('cgtx')
typeGroupedGraphic            = OSType('cpic')
typeInsertionLoc              = OSType('insl')
typeIntlText                  = OSType('itxt')
typeIntlWritingCode           = OSType('intl')
typeLongDateTime              = OSType('ldt ')
typeCFAbsoluteTime            = OSType('cfat')
typeISO8601DateTime           = OSType('isot')
typeLongFixed                 = OSType('lfxd')
typeLongFixedPoint            = OSType('lfpt')
typeLongFixedRectangle        = OSType('lfrc')
typeLongPoint                 = OSType('lpnt')
typeLongRectangle             = OSType('lrct')
typeMachineLoc                = OSType('mLoc')
typeOval                      = OSType('covl')
typeParamInfo                 = OSType('pmin')
typePict                      = OSType('PICT')
typeObjectSpecifier           = OSType('obj ')

typePixelMap                  = OSType('cpix')
typePixMapMinus               = OSType('tpmm')
typePolygon                   = OSType('cpgn')
typePropInfo                  = OSType('pinf')
typePtr                       = OSType('ptr ')
typeQDPoint                   = OSType('QDpt')
typeQDRegion                  = OSType('Qrgn')
typeRectangle                 = OSType('crec')
typeRGB16                     = OSType('tr16')
typeRGB96                     = OSType('tr96')
typeRGBColor                  = OSType('cRGB')
typeRotation                  = OSType('trot')
typeRoundedRectangle          = OSType('crrc')
typeRow                       = OSType('crow')
typeScrapStyles               = OSType('styl')
typeScript                    = OSType('scpt')
typeStyledText                = OSType('STXT')
typeSuiteInfo                 = OSType('suin')
typeTable                     = OSType('ctbl')
typeTextStyles                = OSType('tsty')

typeTIFF                      = OSType('TIFF')
typeJPEG                      = OSType('JPEG')
typeGIF                       = OSType('GIFf')
typeVersion                   = OSType('vers')

kAEMenuClass                  = OSType('menu')
kAEMenuSelect                 = OSType('mhit')
kAEMouseDown                  = OSType('mdwn')
kAEMouseDownInBack            = OSType('mdbk')
kAEKeyDown                    = OSType('kdwn')
kAEResized                    = OSType('rsiz')
kAEPromise                    = OSType('prom')

keyMenuID                     = OSType('mid ')
keyMenuItem                   = OSType('mitm')
keyCloseAllWindows            = OSType('caw ')
keyOriginalBounds             = OSType('obnd')
keyNewBounds                  = OSType('nbnd')
keyLocalWhere                 = OSType('lwhr')

typeHIMenu                    = OSType('mobj')
typeHIWindow                  = OSType('wobj')

kAEQuitReason                 = OSType('why?')

kBySmallIcon                  = 0
kByIconView                   = 1
kByNameView                   = 2
kByDateView                   = 3
kBySizeView                   = 4
kByKindView                   = 5
kByCommentView                = 6
kByLabelView                  = 7
kByVersionView                = 8

kAEInfo                       = 11
kAEMain                       = 0
kAESharing                    = 13

kAEZoomIn                     = 7
kAEZoomOut                    = 8

kTextServiceClass             = OSType('tsvc')
kUpdateActiveInputArea        = OSType('updt')
kShowHideInputWindow          = OSType('shiw')
kPos2Offset                   = OSType('p2st')
kOffset2Pos                   = OSType('st2p')
kUnicodeNotFromInputMethod    = OSType('unim')
kGetSelectedText              = OSType('gtxt')
keyAETSMDocumentRefcon        = OSType('refc')
keyAEServerInstance           = OSType('srvi')
keyAETheData                  = OSType('kdat')
keyAEFixLength                = OSType('fixl')
keyAEUpdateRange              = OSType('udng')
keyAECurrentPoint             = OSType('cpos')
keyAEBufferSize               = OSType('buff')
keyAEMoveView                 = OSType('mvvw')
keyAENextBody                 = OSType('nxbd')
keyAETSMScriptTag             = OSType('sclg')
keyAETSMTextFont              = OSType('ktxf')
keyAETSMTextFMFont            = OSType('ktxm')
keyAETSMTextPointSize         = OSType('ktps')
keyAETSMEventRecord           = OSType('tevt')
keyAETSMEventRef              = OSType('tevr')
keyAETextServiceEncoding      = OSType('tsen')
keyAETextServiceMacEncoding   = OSType('tmen')
keyAETSMGlyphInfoArray        = OSType('tgia')
typeTextRange                 = OSType('txrn')
typeComponentInstance         = OSType('cmpi')
typeOffsetArray               = OSType('ofay')
typeTextRangeArray            = OSType('tray')
typeLowLevelEventRecord       = OSType('evtr')
typeGlyphInfoArray            = OSType('glia')
typeEventRef                  = OSType('evrf')
typeText                      = OSType('')

kTSMOutsideOfBody               = 1
kTSMInsideOfBody                = 2
kTSMInsideOfActiveInputArea     = 3

kNextBody                       = 1
kPreviousBody                   = 2

kTSMHiliteCaretPosition         = 1
kTSMHiliteRawText               = 2
kTSMHiliteSelectedRawText       = 3
kTSMHiliteConvertedText         = 4
kTSMHiliteSelectedConvertedText = 5
kTSMHiliteBlockFillText         = 6
kTSMHiliteOutlineText           = 7
kTSMHiliteSelectedText          = 8
kTSMHiliteNoHilite              = 9

kCaretPosition                = kTSMHiliteCaretPosition
kRawText                      = kTSMHiliteRawText
kSelectedRawText              = kTSMHiliteSelectedRawText
kConvertedText                = kTSMHiliteConvertedText
kSelectedConvertedText        = kTSMHiliteSelectedConvertedText
kBlockFillText                = kTSMHiliteBlockFillText
kOutlineText                  = kTSMHiliteOutlineText
kSelectedText                 = kTSMHiliteSelectedText

keyAEHiliteRange              = OSType('hrng')
keyAEPinRange                 = OSType('pnrg')
keyAEClauseOffsets            = OSType('clau')
keyAEOffset                   = OSType('ofst')
keyAEPoint                    = OSType('gpos')
keyAELeftSide                 = OSType('klef')
keyAERegionClass              = OSType('rgnc')
keyAEDragging                 = OSType('bool')

keyAELeadingEdge              = keyAELeftSide

typeMeters                    = OSType('metr')
typeInches                    = OSType('inch')
typeFeet                      = OSType('feet')
typeYards                     = OSType('yard')
typeMiles                     = OSType('mile')
typeKilometers                = OSType('kmtr')
typeCentimeters               = OSType('cmtr')
typeSquareMeters              = OSType('sqrm')
typeSquareFeet                = OSType('sqft')
typeSquareYards               = OSType('sqyd')
typeSquareMiles               = OSType('sqmi')
typeSquareKilometers          = OSType('sqkm')
typeLiters                    = OSType('litr')
typeQuarts                    = OSType('qrts')
typeGallons                   = OSType('galn')
typeCubicMeters               = OSType('cmet')
typeCubicFeet                 = OSType('cfet')
typeCubicInches               = OSType('cuin')
typeCubicCentimeter           = OSType('ccmt')
typeCubicYards                = OSType('cyrd')
typeKilograms                 = OSType('kgrm')
typeGrams                     = OSType('gram')
typeOunces                    = OSType('ozs ')
typePounds                    = OSType('lbs ')
typeDegreesC                  = OSType('degc')
typeDegreesF                  = OSType('degf')
typeDegreesK                  = OSType('degk')

kFAServerApp                  = OSType('ssrv')
kDoFolderActionEvent          = OSType('fola')
kFolderActionCode             = OSType('actn')
kFolderOpenedEvent            = OSType('fopn')
kFolderClosedEvent            = OSType('fclo')
kFolderWindowMovedEvent       = OSType('fsiz')
kFolderItemsAddedEvent        = OSType('fget')
kFolderItemsRemovedEvent      = OSType('flos')
kItemList                     = OSType('flst')
kNewSizeParameter             = OSType('fnsz')
kFASuiteCode                  = OSType('faco')
kFAAttachCommand              = OSType('atfa')
kFARemoveCommand              = OSType('rmfa')
kFAEditCommand                = OSType('edfa')
kFAFileParam                  = OSType('faal')
kFAIndexParam                 = OSType('indx')

kAEInternetSuite              = OSType('gurl')
kAEISWebStarSuite             = 0x575757BD

kAEISGetURL                   = OSType('gurl')
KAEISHandleCGI                = OSType('sdoc')

cURL                          = OSType('url ')
cInternetAddress              = OSType('IPAD')
cHTML                         = OSType('html')
cFTPItem                      = OSType('ftp ')

kAEISHTTPSearchArgs           = OSType('kfor')
kAEISPostArgs                 = OSType('post')
kAEISMethod                   = OSType('meth')
kAEISClientAddress            = OSType('addr')
kAEISUserName                 = OSType('user')
kAEISPassword                 = OSType('pass')
kAEISFromUser                 = OSType('frmu')
kAEISServerName               = OSType('svnm')
kAEISServerPort               = OSType('svpt')
kAEISScriptName               = OSType('scnm')
kAEISContentType              = OSType('ctyp')
kAEISReferrer                 = OSType('refr')
kAEISUserAgent                = OSType('Agnt')
kAEISAction                   = OSType('Kact')
kAEISActionPath               = OSType('Kapt')
kAEISClientIP                 = OSType('Kcip')
kAEISFullRequest              = OSType('Kfrq')

pScheme                       = OSType('pusc')
pHost                         = OSType('HOST')
pPath                         = OSType('FTPc')
pUserName                     = OSType('RAun')
pUserPassword                 = OSType('RApw')
pDNSForm                      = OSType('pDNS')
pURL                          = OSType('pURL')
pTextEncoding                 = OSType('ptxe')
pFTPKind                      = OSType('kind')

eScheme                       = OSType('esch')
eurlHTTP                      = OSType('http')
eurlHTTPS                     = OSType('htps')
eurlFTP                       = OSType('ftp ')
eurlMail                      = OSType('mail')
eurlFile                      = OSType('file')
eurlGopher                    = OSType('gphr')
eurlTelnet                    = OSType('tlnt')
eurlNews                      = OSType('news')
eurlSNews                     = OSType('snws')
eurlNNTP                      = OSType('nntp')
eurlMessage                   = OSType('mess')
eurlMailbox                   = OSType('mbox')
eurlMulti                     = OSType('mult')
eurlLaunch                    = OSType('laun')
eurlAFP                       = OSType('afp ')
eurlAT                        = OSType('at  ')
eurlEPPC                      = OSType('eppc')
eurlRTSP                      = OSType('rtsp')
eurlIMAP                      = OSType('imap')
eurlNFS                       = OSType('unfs')
eurlPOP                       = OSType('upop')
eurlLDAP                      = OSType('uldp')
eurlUnknown                   = OSType('url?')

kConnSuite                    = OSType('macc')
cDevSpec                      = OSType('cdev')
cAddressSpec                  = OSType('cadr')
cADBAddress                   = OSType('cadb')
cAppleTalkAddress             = OSType('cat ')
cBusAddress                   = OSType('cbus')
cEthernetAddress              = OSType('cen ')
cFireWireAddress              = OSType('cfw ')
cIPAddress                    = OSType('cip ')
cLocalTalkAddress             = OSType('clt ')
cSCSIAddress                  = OSType('cscs')
cTokenRingAddress             = OSType('ctok')
cUSBAddress                   = OSType('cusb')

pDeviceType                   = OSType('pdvt')
pDeviceAddress                = OSType('pdva')
pConduit                      = OSType('pcon')
pProtocol                     = OSType('pprt')
pATMachine                    = OSType('patm')
pATZone                       = OSType('patz')
pATType                       = OSType('patt')
pDottedDecimal                = OSType('pipd')
pDNS                          = OSType('pdns')
pPort                         = OSType('ppor')
pNetwork                      = OSType('pnet')
pNode                         = OSType('pnod')
pSocket                       = OSType('psoc')
pSCSIBus                      = OSType('pscb')
pSCSILUN                      = OSType('pslu')

eDeviceType                   = OSType('edvt')
eAddressSpec                  = OSType('eads')
eConduit                      = OSType('econ')
eProtocol                     = OSType('epro')
eADB                          = OSType('eadb')
eAnalogAudio                  = OSType('epau')
eAppleTalk                    = OSType('epat')
eAudioLineIn                  = OSType('ecai')
eAudioLineOut                 = OSType('ecal')
eAudioOut                     = OSType('ecao')
eBus                          = OSType('ebus')
eCDROM                        = OSType('ecd ')
eCommSlot                     = OSType('eccm')
eDigitalAudio                 = OSType('epda')
eDisplay                      = OSType('edds')
eDVD                          = OSType('edvd')
eEthernet                     = OSType('ecen')
eFireWire                     = OSType('ecfw')
eFloppy                       = OSType('efd ')
eHD                           = OSType('ehd ')
eInfrared                     = OSType('ecir')
eIP                           = OSType('epip')
eIrDA                         = OSType('epir')
eIRTalk                       = OSType('epit')
eKeyboard                     = OSType('ekbd')
eLCD                          = OSType('edlc')
eLocalTalk                    = OSType('eclt')
eMacIP                        = OSType('epmi')
eMacVideo                     = OSType('epmv')
eMicrophone                   = OSType('ecmi')
eModemPort                    = OSType('ecmp')
eModemPrinterPort             = OSType('empp')
eModem                        = OSType('edmm')
eMonitorOut                   = OSType('ecmn')
eMouse                        = OSType('emou')
eNuBusCard                    = OSType('ednb')
eNuBus                        = OSType('enub')
ePCcard                       = OSType('ecpc')
ePCIbus                       = OSType('ecpi')
ePCIcard                      = OSType('edpi')
ePDSslot                      = OSType('ecpd')
ePDScard                      = OSType('epds')
ePointingDevice               = OSType('edpd')
ePostScript                   = OSType('epps')
ePPP                          = OSType('eppp')
ePrinterPort                  = OSType('ecpp')
ePrinter                      = OSType('edpr')
eSvideo                       = OSType('epsv')
eSCSI                         = OSType('ecsc')
eSerial                       = OSType('epsr')
eSpeakers                     = OSType('edsp')
eStorageDevice                = OSType('edst')
eSVGA                         = OSType('epsg')
eTokenRing                    = OSType('etok')
eTrackball                    = OSType('etrk')
eTrackpad                     = OSType('edtp')
eUSB                          = OSType('ecus')
eVideoIn                      = OSType('ecvi')
eVideoMonitor                 = OSType('edvm')
eVideoOut                     = OSType('ecvo')

cKeystroke                    = OSType('kprs')
pKeystrokeKey                 = OSType('kMsg')
pModifiers                    = OSType('kMod')
pKeyKind                      = OSType('kknd')
eModifiers                    = OSType('eMds')
eOptionDown                   = OSType('Kopt')
eCommandDown                  = OSType('Kcmd')
eControlDown                  = OSType('Kctl')
eShiftDown                    = OSType('Ksft')
eCapsLockDown                 = OSType('Kclk')
eKeyKind                      = OSType('ekst')

eEscapeKey                    = 0x6B733500
eDeleteKey                    = 0x6B733300
eTabKey                       = 0x6B733000
eReturnKey                    = 0x6B732400
eClearKey                     = 0x6B734700
eEnterKey                     = 0x6B734C00
eUpArrowKey                   = 0x6B737E00
eDownArrowKey                 = 0x6B737D00
eLeftArrowKey                 = 0x6B737B00
eRightArrowKey                = 0x6B737C00
eHelpKey                      = 0x6B737200
eHomeKey                      = 0x6B737300
ePageUpKey                    = 0x6B737400
ePageDownKey                  = 0x6B737900
eForwardDelKey                = 0x6B737500
eEndKey                       = 0x6B737700
eF1Key                        = 0x6B737A00
eF2Key                        = 0x6B737800
eF3Key                        = 0x6B736300
eF4Key                        = 0x6B737600
eF5Key                        = 0x6B736000
eF6Key                        = 0x6B736100
eF7Key                        = 0x6B736200
eF8Key                        = 0x6B736400
eF9Key                        = 0x6B736500
eF10Key                       = 0x6B736D00
eF11Key                       = 0x6B736700
eF12Key                       = 0x6B736F00
eF13Key                       = 0x6B736900
eF14Key                       = 0x6B736B00
eF15Key                       = 0x6B737100

keyAELaunchedAsLogInItem      = OSType('lgit')
keyAELaunchedAsServiceItem    = OSType('svit')

keyDirectObject               = OSType('----')
keyErrorNumber                = OSType('errn')
keyErrorString                = OSType('errs')
keyProcessSerialNumber        = OSType('psn ')
keyPreDispatch                = OSType('phac')
keySelectProc                 = OSType('selh')

keyAERecorderCount            = OSType('recr')

keyAEVersion                  = OSType('vers')

kCoreEventClass               = OSType('aevt')

kAEOpenApplication            = OSType('oapp')
kAEOpenDocuments              = OSType('odoc')
kAEPrintDocuments             = OSType('pdoc')
kAEOpenContents               = OSType('ocon')
kAEQuitApplication            = OSType('quit')

kAEAnswer                     = OSType('ansr')
kAEApplicationDied            = OSType('obit')
kAEShowPreferences            = OSType('pref')

kAEStartRecording             = OSType('reca')
kAEStopRecording              = OSType('recc')
kAENotifyStartRecording       = OSType('rec1')
kAENotifyStopRecording        = OSType('rec0')
kAENotifyRecording            = OSType('recr')

kAEUnknownSource              = 0
kAEDirectCall                 = 1
kAESameProcess                = 2
kAELocalProcess               = 3
kAERemoteProcess              = 4
typeUnicodeText = 0x75747874
keyAEKeyForm = 0x666F726D
keyAEDesiredClass = 0x77616E74

errAETargetAddressNotPermitted	 = 	-1742
errAEEventNotPermitted = -1743

formPropertyID = OSType('prop')
formName       = OSType('name')
keyAEIndex = 0x6B696478

def event_from_int(i: int) -> ApplicationServices.NSAppleEventDescriptor:
    """Creates an Apple Event descriptor of event type typeSInt32 that stores the provided integer.

    .. versionadded:: 0.0.4
    """
    return ApplicationServices.NSAppleEventDescriptor.descriptorWithInt32_(i)

def event_from_str(s: str) -> ApplicationServices.NSAppleEventDescriptor:
    """Creates an Apple Event descriptor of event type typeUnicodeText that stores the provided string.

    .. versionadded:: 0.0.4
    """
    return ApplicationServices.NSAppleEventDescriptor.descriptorWithString_(s)

def event_from_bool(b: bool) -> ApplicationServices.NSAppleEventDescriptor:
    """Creates an Apple Event descriptor of event type typeBoolean that stores the provided boolean value.

    .. versionadded:: 0.0.4
    """
    return ApplicationServices.NSAppleEventDescriptor.descriptorWithBoolean_(b)

def xaevent_activate_app_by_bundle_id(paths: List[str]):
    send_event_to_bundle(kAEMiscStandards, kAEActivate, "com.apple.MobileSMS")

def xaevent_reopen_app_by_bundle_id(paths: List[str]):
    send_event_to_bundle(typeAppleEvent, kAEReopenApplication, "com.apple.MobileSMS")

def xaevent_open_in_app_by_bundle_id(path: str, bundle_id: str):
    app_desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeApplicationBundleID, "com.apple.TextEdit".encode("UTF-8"))

    openEvent = ApplicationServices.NSAppleEventDescriptor.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_(typeAppleEvent, kAEOpenDocuments, app_desc, kAutoGenerateReturnID, kAnyTransactionID)

    url = NSURL.alloc().initFileURLWithPath_(path)
    desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeFileURL, url.absoluteString().encode("UTF-8"))

    openEvent.setParamDescriptor_forKeyword_(desc, keyDirectObject)
    openEvent.sendEventWithOptions_timeout_error_(kAEWaitReply|kAECanInteract, kAEDefaultTimeout, None)

def xaevent_print_immediately_from_app_by_bundle_id(path: str, bundle_id: str):
    app_desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeApplicationBundleID, "com.apple.TextEdit".encode("UTF-8"))

    openEvent = ApplicationServices.NSAppleEventDescriptor.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_(typeAppleEvent, kAEPrintDocuments, app_desc, kAutoGenerateReturnID, kAnyTransactionID)

    url = NSURL.alloc().initFileURLWithPath_(path)
    desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeFileURL, url.absoluteString().encode("UTF-8"))

    openEvent.setParamDescriptor_forKeyword_(desc, keyDirectObject)
    openEvent.sendEventWithOptions_timeout_error_(kAEWaitReply|kAECanInteract, kAEDefaultTimeout, None)

def test():
    # Target
    app_desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeApplicationBundleID, "com.apple.Safari".encode("UTF-8"))

    openEvent = ApplicationServices.NSAppleEventDescriptor.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_(typeAppleEvent, kAEZoomIn, app_desc, kAutoGenerateReturnID, kAnyTransactionID)

    # keyData = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(cSelection)

    # test =  ApplicationServices.NSAppleEventDescriptor.alloc().initRecordDescriptor()
    # test.setParamDescriptor_forKeyword_(keyData, cProperty)

    # initWithContainerSpecifier_key_(ApplicationServices.NSScriptObjectSpecifier.alloc().init(), formPropertyID)
    # doc_desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeObjectSpecifier, "cDocument".encode("UTF-8"))
    # openEvent.setParamDescriptor_forKeyword_(app_desc, keyAEInsertHere)
    # docu_desc.setAssociatedObject_(doc)

    # doc = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(cDocument)
    # obj = ApplicationServices.NSScriptObjectSpecifier.objectSpecifierWithDescriptor_(doc)
    # test = ApplicationServices.NSScriptObjectSpecifier.alloc().initWithContainerSpecifier_key_(obj, formName)

    # doc = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(cDocument)
    # # # record = ApplicationServices.NSAppleEventDescriptor.alloc().initRecordDescriptor()
    # # # doc = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(cDocument)
    # # # record.insertDescriptor_atIndex_(doc, 1)
    # # # print(record)
    # # record = ApplicationServices.NSAppleEventDescriptor.alloc().initRecordDescriptor()
    # # record.setParamDescriptor_forKeyword_(doc, typeObjectSpecifier)

    # openEvent.setParamDescriptor_forKeyword_(doc, keyAEObjectClass)

    print(openEvent)
    test = openEvent.sendEventWithOptions_timeout_error_(kAEWaitReply|kAECanInteract, kAEDefaultTimeout, None)

    print(test)

def get_selection(bundle_id: str):
    app_desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeApplicationBundleID, bundle_id.encode("UTF-8"))

    openEvent = ApplicationServices.NSAppleEventDescriptor.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_(kAECoreSuite, kAEGetData, app_desc, kAutoGenerateReturnID, kAnyTransactionID)

    # doc = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(cDocument)
    # openEvent.setParamDescriptor_forKeyword_(doc, keyAEObjectClass)

    record = ApplicationServices.NSAppleEventDescriptor.alloc().initRecordDescriptor()
    prop1 = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(OSType('indx'))
    prop2 = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(OSType('cwin'))

    sele = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(OSType('abso'), bytes(' lla'.encode("UTF-8")))

    nul = ApplicationServices.NSAppleEventDescriptor.nullDescriptor()

    record.setDescriptor_forKeyword_(prop1, OSType('form'))
    record.setDescriptor_forKeyword_(prop2, OSType('want'))
    record.setDescriptor_forKeyword_(sele, OSType('seld'))
    record.setDescriptor_forKeyword_(nul, OSType('from'))

    # print(record)

    # print(bytes.fromhex('206C6C61').decode('utf-8'))

    # test = ApplicationServices.NSScriptObjectSpecifier.objectSpecifierWithDescriptor_(record)
    # print(test)

    # obj = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(typeObjectSpecifier)

    #obj = record.coerceToDescriptorType_(typeObjectSpecifier)
    obj = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(typeObjectSpecifier)
    # obj.setDescriptor_forKeyword_(prop1, OSType('form'))
    # obj.setDescriptor_forKeyword_(prop2, OSType('want'))
    # obj.setDescriptor_forKeyword_(sele, OSType('seld'))
    # obj.setDescriptor_forKeyword_(nul, OSType('from'))

    # app_desc = ApplicationServices.NSScriptClassDescription.classDescriptionForClass_(NSapp.__class__)
    # test = ApplicationServices.NSScriptObjectSpecifier.alloc().initWithContainerClassDescription_containerSpecifier_key_(record, "windows", )
    # print(test)
    # print(obj)

    test = ApplicationServices.NSAppleEventDescriptor.alloc().initWithAEDescNoCopy_(record.aeDesc())

    openEvent.setParamDescriptor_forKeyword_(obj, keyDirectObject)

    sig = ApplicationServices.NSAppleEventDescriptor.descriptorWithInt32_(65536)
    openEvent.setAttributeDescriptor_forKeyword_(sig, OSType('csig'))
    
    print(openEvent.description())
    test = openEvent.sendEventWithOptions_timeout_error_(kAEWaitReply|kAECanInteract, kAEDefaultTimeout, None)
    print(test)

def get_window_title(bundle_id: str):
    app_desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeApplicationBundleID, bundle_id.encode("UTF-8"))

    openEvent = ApplicationServices.NSAppleEventDescriptor.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_(kAECoreSuite, kAEGetData, app_desc, kAutoGenerateReturnID, kAnyTransactionID)

    # doc = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(cDocument)
    # openEvent.setParamDescriptor_forKeyword_(doc, keyAEObjectClass)

    record = ApplicationServices.NSAppleEventDescriptor.alloc().initRecordDescriptor()
    indx = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(OSType('indx'))
    #indx = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(OSType('cwin'))
    cwin = ApplicationServices.NSAppleEventDescriptor.descriptorWithEnumCode_(pSelection)
    seld = ApplicationServices.NSAppleEventDescriptor.descriptorWithInt32_(1)
    # seld = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(cDocument)
    #seld = ApplicationServices.NSAppleEventDescriptor.descriptorWithString_("name")

    want = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(cWindow)
    record.setParamDescriptor_forKeyword_(want, keyAEDesiredClass)

    form = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(OSType('indx'))
    record.setParamDescriptor_forKeyword_(form, keyAEKeyForm)

    from_ = ApplicationServices.NSAppleEventDescriptor.nullDescriptor()
    record.setParamDescriptor_forKeyword_(from_, OSType('from'))

    seld = ApplicationServices.NSAppleEventDescriptor.descriptorWithInt32_(1)
    record.setParamDescriptor_forKeyword_(seld, OSType('seld'))

    # obj = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(typeObjectSpecifier)

    obj = record.coerceToDescriptorType_(typeObjectSpecifier)

    # print(obj)

    #print(OSType('brow'))
    #test = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeObjectSpecifier, )

    openEvent.setParamDescriptor_forKeyword_(obj, keyDirectObject)

    sig = ApplicationServices.NSAppleEventDescriptor.descriptorWithInt32_(65536)
    openEvent.setAttributeDescriptor_forKeyword_(sig, OSType('csig'))
    
    print(openEvent.description())
    test = openEvent.sendEventWithOptions_timeout_error_(kAEWaitReply|kAECanInteract, kAEDefaultTimeout, None)
    print(test)

    answer = test[0].descriptorAtIndex_(1)

    # obj = answer.coerceToDescriptorType_(typeAERecord)
   

def get_window(bundle_id: str):
    app_desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeApplicationBundleID, bundle_id.encode("UTF-8"))

    openEvent = ApplicationServices.NSAppleEventDescriptor.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_(kAECoreSuite, kAEGetData, app_desc, kAutoGenerateReturnID, kAnyTransactionID)

    # doc = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(cDocument)
    # openEvent.setParamDescriptor_forKeyword_(doc, keyAEObjectClass)

    record = ApplicationServices.NSAppleEventDescriptor.alloc().initRecordDescriptor()
    indx = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(OSType('indx'))
    #indx = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(OSType('cwin'))
    cwin = ApplicationServices.NSAppleEventDescriptor.descriptorWithEnumCode_(pSelection)
    seld = ApplicationServices.NSAppleEventDescriptor.descriptorWithInt32_(1)
    # seld = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(cDocument)
    #seld = ApplicationServices.NSAppleEventDescriptor.descriptorWithString_("name")
    nul = ApplicationServices.NSAppleEventDescriptor.nullDescriptor()
    record.setParamDescriptor_forKeyword_(nul, OSType('from'))

    want = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(OSType('prop'))
    record.setParamDescriptor_forKeyword_(want, keyAEDesiredClass)

    form = ApplicationServices.NSAppleEventDescriptor.descriptorWithEnumCode_(OSType('prop'))
    record.setParamDescriptor_forKeyword_(form, keyAEKeyForm)

    seld = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(pSelection)
    record.setParamDescriptor_forKeyword_(seld, OSType('seld'))

    # obj = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(typeObjectSpecifier)

    obj = record.coerceToDescriptorType_(typeObjectSpecifier)

    # print(obj)

    #print(OSType('brow'))
    #test = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeObjectSpecifier, )

    openEvent.setParamDescriptor_forKeyword_(obj, keyDirectObject)

    sig = ApplicationServices.NSAppleEventDescriptor.descriptorWithInt32_(65536)
    openEvent.setAttributeDescriptor_forKeyword_(sig, OSType('csig'))
    
    print(openEvent.description())
    test = openEvent.sendEventWithOptions_timeout_error_(kAEWaitReply|kAECanInteract, kAEDefaultTimeout, None)
    print(test)
    
    record = test[0].descriptorAtIndex_(1).coerceToDescriptorType_(typeAERecord)

    print(traverse(record))

def traverse(descriptor):
    ret = ""
    for x in range(1, descriptor.numberOfItems() + 1):
        desc = descriptor.descriptorAtIndex_(x)
        # print(desc.descriptorType() == typeEnumeration)
        if desc.descriptorType() == typeUnicodeText and desc.stringValue() is not None:
            ret += "/"+desc.stringValue()
        ret += traverse(desc)
    return ret

    # data = NSData.alloc().initWithBytes_length_(test[0].data(), len(test[0].data()))

    # # z = None
    # # blah = data.getBytes_length_(z, data.length())
    # AEDescRef = objc.createOpaquePointerType(
    #     "AEDescRef", b"^{AEDesc=I^^{OpaqueAEDataStorageType}}"
    # )
    # # print(blah.decode())
    # # objc.objc_object(c_void_p = test[0].descriptorAtIndex_(1).aeDesc().__c_void_p__())
    # print(test[0].descriptorAtIndex_(1).descriptorAtIndex_(1).typeCodeValue())

def xaevent_minimize_app(bundle_id: str, param: Any = None):
    app_desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeApplicationBundleID, bundle_id.encode("UTF-8"))

    openEvent = ApplicationServices.NSAppleEventDescriptor.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_(kAECoreSuite, kAECreateElement, app_desc, kAutoGenerateReturnID, kAnyTransactionID)

    doc = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(cDocument)
    openEvent.setParamDescriptor_forKeyword_(doc, keyAEObjectClass)

    record = ApplicationServices.NSAppleEventDescriptor.alloc().initRecordDescriptor()
    name = ApplicationServices.NSAppleEventDescriptor.descriptorWithString_(param)
    record.setParamDescriptor_forKeyword_(name, keyAEName)

    openEvent.setParamDescriptor_forKeyword_(record, keyAEPropData)
    
    print(openEvent)
    test = openEvent.sendEventWithOptions_timeout_error_(kAEWaitReply|kAECanInteract, kAEDefaultTimeout, None)

def xaevent_create_new_doc_named(bundle_id: str, param: Any = None):
    app_desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeApplicationBundleID, bundle_id.encode("UTF-8"))

    openEvent = ApplicationServices.NSAppleEventDescriptor.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_(kAECoreSuite, kAECreateElement, app_desc, kAutoGenerateReturnID, kAnyTransactionID)

    doc = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(cDocument)
    openEvent.setParamDescriptor_forKeyword_(doc, keyAEObjectClass)

    record = ApplicationServices.NSAppleEventDescriptor.alloc().initRecordDescriptor()
    name = ApplicationServices.NSAppleEventDescriptor.descriptorWithString_(param)
    record.setParamDescriptor_forKeyword_(name, keyAEName)

    openEvent.setParamDescriptor_forKeyword_(record, keyAEPropData)
    
    print(openEvent)
    test = openEvent.sendEventWithOptions_timeout_error_(kAEWaitReply|kAECanInteract, kAEDefaultTimeout, None)

def xaevent_create_new(bundle_id: str, specifier: str, param: Any = None):
    app_desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeApplicationBundleID, bundle_id.encode("UTF-8"))

    openEvent = ApplicationServices.NSAppleEventDescriptor.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_(kAECoreSuite, kAECreateElement, app_desc, kAutoGenerateReturnID, kAnyTransactionID)

    doc = ApplicationServices.NSAppleEventDescriptor.descriptorWithString_(specifier)
    openEvent.setParamDescriptor_forKeyword_(doc, keyAEObjectClass)

    record = ApplicationServices.NSAppleEventDescriptor.alloc().initRecordDescriptor()
    text = ApplicationServices.NSAppleEventDescriptor.descriptorWithString_(param)
    #name = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(keyAEName, param.encode("UTF-8"))
    record.setParamDescriptor_forKeyword_(text, keyAEName)
    # record.setParamDescriptor_forKeyword_(text, OSType('body'))

    openEvent.setParamDescriptor_forKeyword_(record, keyAEPropData)
    
    print(openEvent)
    test = openEvent.sendEventWithOptions_timeout_error_(kAEWaitReply|kAECanInteract, kAEDefaultTimeout, None)

def xaevent_create_new_document(bundle_id: str):
    app_desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeApplicationBundleID, bundle_id.encode("UTF-8"))

    openEvent = ApplicationServices.NSAppleEventDescriptor.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_(kAECoreSuite, kAECreateElement, app_desc, kAutoGenerateReturnID, kAnyTransactionID)

    doc = ApplicationServices.NSAppleEventDescriptor.descriptorWithTypeCode_(cDocument)
    openEvent.setParamDescriptor_forKeyword_(doc, keyAEObjectClass)

    test = openEvent.sendEventWithOptions_timeout_error_(kAEWaitReply|kAECanInteract, kAEDefaultTimeout, None)

def xaevent_open_items_at_paths(paths: List[str]):
    app_desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeApplicationBundleID, "com.apple.Finder".encode("UTF-8"))

    fileList = ApplicationServices.NSAppleEventDescriptor.listDescriptor()
    openEvent = ApplicationServices.NSAppleEventDescriptor.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_(typeAppleEvent, kAEOpenDocuments, app_desc, kAutoGenerateReturnID, kAnyTransactionID)

    for path in paths:
        url = NSURL.alloc().initFileURLWithPath_(path)
        desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeFileURL, url.absoluteString().encode("UTF-8"))
        fileList.insertDescriptor_atIndex_(desc, 0)

    openEvent.setParamDescriptor_forKeyword_(fileList, keyDirectObject)
    openEvent.sendEventWithOptions_timeout_error_(kAEWaitReply|kAECanInteract, kAEDefaultTimeout, None)