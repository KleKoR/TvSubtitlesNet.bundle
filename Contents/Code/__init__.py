#xsubs.tv

import string, os, re, zipfile #urllib, zipfile, copy

OS_PLEX_USERAGENT = 'plexapp.com v9.0'

seriesList = {}

langPlexTvsub = {
    'ar' : 'ar',
    'br' : 'br',
    'bg' : 'bg',
    'nl' : 'nl',
    'en' : 'en',
    'fr' : 'fr',
    'de' : 'de',
    'el' : 'gr',
    'hu' : 'hu',
    'it' : 'it',
    'ko' : 'ko',
    'pl' : 'pl',
    'pt' : 'pt',
    'ro' : 'ro',
    'ru' : 'ru',
    'es' : 'es',
    'tr' : 'tr',
    'uk' : 'ua'
}

resolDict = {
    '720p' : ['HDTV', 'BluRay', 'WEB-DL', 'WEBRip', 'HDDVD', 'BRRip', 'WEB-Rip'],
    '1080p' : ['BluRay', 'WEB-DL', 'WEBRip', 'WS', 'HDTV'],
    '480p' : ['HDTV', 'WEB-DL', 'BluRay', 'WEBRip'],
    '1080i' : ['HDTV'],
    '576p' : ['HDTV']
}

sourceDict = {
    'dvdrip' : ['x264', 'XviD'],
    'hdtv' : ['720p', 'XviD', 'x264', '480p', '1080i', '1080p', 'DivX', '576p'],
    'bluray' : ['720p', '1080p', '480p', 'XviD'],
    'web-dl' : ['720p', '1080p', '480p', 'x264', 'XviD', 'H264'],
    'webrip' : ['720p', '1080p', 'x264', 'XviD', '480p'],
    'pdtv' : ['HR', 'x264', 'XviD'],
    'bdrip' : ['x264', 'XviD', 'WS'],
    'tvrip' : [],
    'hddvd' : ['720p'],
    'dvdscr' : [],
    'web-rip' : ['720p'],
    'ws' : ['1080p', 'BDRip', 'XviD']
}

encDict = {
    'xvid' : ['HDTV', 'DVDRip', 'BDRip', 'WEBRip', 'WEB-DL', 'PDTV', 'AC3', 'WS', 'BluRay'],
    'x264' : ['HDTV', 'DVDRip', 'BDRip', 'WEBRip', 'WEB-DL', 'PDTV'],
    'h264' : ['WEB-DL'],
    'divx' : ['HDTV']
}

encTypesReplaceDict = {
    'dvdrip' : 'DVDRip',
    'hdtv' : 'HDTV',
    'xvid' : 'XviD',
    'x264' : 'x264',
    'bluray' : 'BluRay',
    'web-dl' : 'WEB-DL',
    'webrip' : 'WEBRip',
    'pdtv' : 'PDTV',
    'bdrip' : 'BDRip',
    'dsr' : 'DSR',
    'ws' : 'WS',
    'brrip' : 'BRRip',
    'hr' : 'HR',
    'tvrip' : 'TVRip',
    'hddvd' : 'HDDVD',
    'h264' : 'H264',
    'dvdscr' : 'DVDSCR',
    'ac3' : 'AC3',
    'divx' : 'DivX',
    'web-rip' : 'WEB-Rip'
}

#unused
encTypesDict = {
    'DVDRip' : ['x264', 'XviD'],
    '720p' : ['HDTV', 'BluRay', 'WEB-DL', 'WEBRip', 'HDDVD', 'BRRip', 'WEB-Rip'],
    'HDTV' : ['720p', 'XviD', 'x264', '480p', '1080i', '1080p', 'DivX', '576p'],
    'XviD' : ['HDTV', 'DVDRip', 'BDRip', 'WEBRip', 'WEB-DL', 'PDTV', 'AC3', 'WS', 'BluRay'],
    'x264' : ['HDTV', 'DVDRip', 'BDRip', 'WEBRip', 'WEB-DL', 'PDTV'],
    'BluRay' : ['720p', '1080p', '480p', 'XviD'],
    'WEB-DL' : ['720p', '1080p', '480p', 'x264', 'XviD', 'H264'],
    'WEBRip' : ['720p', '1080p', 'x264', 'XviD', '480p'],
    '1080p' : ['BluRay', 'WEB-DL', 'WEBRip', 'WS', 'HDTV'],
    '480p' : ['HDTV', 'WEB-DL', 'BluRay', 'WEBRip'],
    'PDTV' : ['HR', 'x264', 'XviD'],
    'BDRip' : ['x264', 'XviD', 'WS'],
    'DSR' : [],
    'WS' : ['1080p', 'BDRip', 'XviD'],
    '1080i' : ['HDTV'],
    'BRRip' : ['720p'],
    'HR' : ['PDTV'],
    'TVRip' : [],
    'HDDVD' : ['720p'],
    'H264' : ['WEB-DL'],
    'DVDSCR' : [],
    'AC3' : ['XviD'],
    'DivX' : ['HDTV'],
    'WEB-Rip' : ['720p'],
    '576p' : ['HDTV']
}

dctTeam = {}

def Start():
    HTTP.CacheTime = 0
    HTTP.Headers['User-agent'] = OS_PLEX_USERAGENT
    Log("START CALLED")

def ValidatePrefs():
    return

def getSubUrl(data, language):
    Log('Filename:  '+ data['sFl'])
    sre = getSourceResolutionEncoding(data['sFl'])
    fnlName = findSeriesNameinXsubs(data['sK'])
    if fnlName !='':
        srid = seriesList[fnlName]
    else:
        return

    Log(srid)
    #http://www.tvsubtitles.net/tvshow-870-3.html
    seriesUrl = 'http://www.tvsubtitles.net/tvshow-'+str(srid)+'-'+str(data['sTS'])+'.html'
    Log(seriesUrl)
    elem = HTML.ElementFromURL(seriesUrl)
    #only element of episode only if has greek subs
    #//table[@id='table5']/tbody/tr[td/text()='4x08' and td/nobr/a/img/@src='images/flags/gr.gif']/td[2]
    subpages = elem.xpath("//table[@id='table5']/tr[td/text()='"+str(data['sTS'])+"x"+data['sTE'].zfill(2)+"' and td/nobr/a/img/@src='images/flags/"+langPlexTvsub[language]+".gif']/td[2]")
    if len(subpages)==1:
        Log(subpages[0].xpath('a/@href'))
        episodeUrl = 'http://www.tvsubtitles.net/'+ subpages[0].xpath('a/@href')[0]
        Log("Episode url: "+episodeUrl)
        episodeElem = HTML.ElementFromURL(episodeUrl)
        #//a[div/@class='subtitlen' and div/h5/img/@src='images/flags/gr.gif']
        subsA = episodeElem.xpath("//a[div/@class='subtitlen' and div/h5/img/@src='images/flags/"+langPlexTvsub[language]+".gif']")
        Log(subsA)
        subsInfoList = []
        for l in subsA:
            subInfo = {}
            subId = l.xpath('./@href')[0].split('-')[1].split('.')[0]
            Log(subId)
            rip = l.xpath(".//p[@title='rip']/text()")[0].strip(' \t\n\r')
            Log(rip)
            release = l.xpath(".//p[@title='release']/text()")[0].strip(' \t\n\r')
            Log(release)
            downloaded = l.xpath(".//p[@title='downloaded']/text()")[0].strip(' \t\n\r')
            Log(downloaded)
            #//span[@style = 'color:red']
            good = l.xpath(".//span[@style='color:green']/text()")[0].strip(' \t\n\r')
            Log(good)
            bad = l.xpath(".//span[@style='color:red']/text()")[0].strip(' \t\n\r')
            Log(bad)
            subInfo['id'] = subId
            subInfo['rip'] = rip
            subInfo['release'] = release
            subInfo['downloaded'] = int(downloaded)
            subInfo['good'] = int(good)
            subInfo['bad'] = int(bad)
            subsInfoList.append(subInfo)
        Log(subsInfoList)
        finalList =[]
        for d in subsInfoList:
            ripok = False
            groupOk = False
            if sre['Resolution'] != '':
                if sre['Resolution'] in d['rip']:
                    rip = True
            if data['sR'] != '':
                if data['sR'] in d['release']:
                    groupOk = True
            if rip and groupOk:
                finalList.append(d)
        Log(finalList)
        if len(finalList) == 0:
            return

        sortedFinalList = sorted(finalList, key=lambda k: k['downloaded'], reverse=True)
        #http://www.tvsubtitles.net/download-267721.html
        subUrl  = 'http://www.tvsubtitles.net/download-'+sortedFinalList[0]['id']+'.html'
        Log(subUrl)
        return subUrl

def fillSeriesList():
    #http://www.tvsubtitles.net/tvshows.html
    seriesUrl = 'http://www.tvsubtitles.net/tvshows.html'
    elem = HTML.ElementFromURL(seriesUrl)
    subpages = elem.xpath("//table[@id='table5']/tr/td[2]")
    for l in subpages:
        #Log(l.xpath('a/b/text()')[0])
        #Log(l.xpath('a/@href')[0].split("-")[1])
        seriesList[l.xpath('a/b/text()')[0]] = int(l.xpath('a/@href')[0].split("-")[1])
    Log(seriesList)
    Log(len(seriesList))

def getReleaseGroup(filename):
    tmpFile = string.replace(filename, '-', '.')
    splitName = string.split(tmpFile, '.')
    if ('gttvsd' in splitName[-2].lower()) or ('gtrd'in splitName[-2].lower()) or ('eztv'in splitName[-2].lower()) or ('vtv'in splitName[-2].lower()):
        group = splitName[-3].strip()
    else:
        group = splitName[-2].strip() 
    if 'REPACK' in filename:
        group = 'REPACK '+ group
    if 'PROPER' in filename:
        group = 'PROPER ' + group
    Log("group= " + group)
    return group

def getSourceResolutionEncoding(filename):
    tmpFile = filename.lower()
    splitName = string.split(tmpFile, '.')
    retval = {'Source' : '','Resolution' : '','Encoding' : ''}
    for l in splitName:
        if l in sourceDict:
            Log("Source in SourceDict: " + l)
            retval['Source'] = encTypesReplaceDict[l]
        if l in resolDict:
            retval['Resolution'] = l
        if l in encDict:
            retval['Encoding'] = encTypesReplaceDict[l]
    if retval['Encoding'] == '':
        if '264' in tmpFile:
            retval['Encoding'] = 'x264'
        else:
            Log("if '264' in tmpFile: = FALSE")
            tmpFile = string.replace(filename.lower(), '-', '.')
            splitName = string.split(tmpFile, '.')
            for l in splitName:
                if l in encDict:
                    retval['Encoding'] = encTypesReplaceDict[l]
    if retval['Source'] == '':
        Log("if retval['Source'] == '':")
        tmpFile = string.replace(filename.lower(), '-', '.')
        splitName = string.split(tmpFile, '.')
        for l in splitName:
            if l in sourceDict:
                retval['Source'] = encTypesReplaceDict[l]
    if retval['Resolution'] == '':
        Log("if retval['Resolution'] == '':")
        tmpFile = string.replace(filename.lower(), '-', '.')
        splitName = string.split(tmpFile, '.')
        for l in splitName:
            if l in resolDict:
                retval['Resolution'] = encTypesReplaceDict[l]
    Log("Source: %s" % retval['Source'])
    Log("Resolution: %s" % retval['Resolution'])
    Log("Encoding: %s" % retval['Encoding'])
    return retval

#according to xsubs site
def getAppropriateFmt(fmtValues):
    retval = ''
    if fmtValues['Resolution'] != '':
        retval = fmtValues['Resolution'] + '.' + fmtValues['Source']
        Log("Fmt value: %s" % retval)
        return retval
    else:
        if fmtValues['Source']!= '' and fmtValues['Encoding'] != '':
            retval = fmtValues['Source'] + '.' + fmtValues['Encoding']
            Log("Fmt value: %s" % retval)
            return retval
        if fmtValues['Source']== '':
            retval =  fmtValues['Encoding']
            Log("Fmt value: %s" % retval)
            return retval
        else:
            retval =  fmtValues['Source']
            Log("Fmt value: %s" % retval)
            return retval
    Log("Fmt value: %s" % retval)
    return retval

def findSeriesNameinXsubs(name):
    # try removing parenthesees in given name
    tmpName = name
    tmpName = re.sub(r'\([^)]*\)', '', tmpName).strip()
    sName  = string.split(tmpName,' ')
    srchName = []
    fnlName = ''
    if sName[0].lower() == 'the':
        for i in range(1,len(sName)):
            srchName.append(sName[i])
        #Log(srchName)
        srchName.append('(The)')
        #Log(srchName)
        fnlName  = ' '.join(srchName)
        #Log(fnlName)
    else:
        fnlName = tmpName
    if fnlName in seriesList:
        Log('1 Original name: ' + name + '    found name: ' + fnlName)
        return fnlName
    for key, value in seriesList.iteritems():
        if re.sub(r'\[[^)]*\]', '', key).lower().strip() == fnlName.lower():
            Log('2 Original name: ' + name + '    found name: ' + key)
            return key


    tmpDict = {}
    splName  = string.split(name,' ')
    for key, value in seriesList.iteritems():
        for wrd in splName:
            if len(wrd)<3:
                continue
            if wrd=='' or wrd.lower()=='the'or wrd.lower()=='and':
                continue
            if wrd in key:
                if key in tmpDict:
                    tmpDict[key].append(wrd)
                else:
                    tmpDict[key] = [wrd]
    count = 0
    hgName = ''
    for key,value in tmpDict.iteritems():
        if len(value)> count:
            count = len(value)
            hgName = key
    if count > 1:
        Log('3 Original name: ' + name + '    found name: ' + hgName)
        return hgName
    return ''





class XsubsSubtitlesAgentTvShows(Agent.TV_Shows):
    name = 'TVsubtitles.net TV Subtitles'
    languages = [Locale.Language.Greek]
    primary_provider = False
    contributes_to = ['com.plexapp.agents.thetvdb']

    def search(self, results, media, lang):
        Log("TV SEARCH CALLED")
        results.Append(MetadataSearchResult(id = 'null', score = 100))

    def update(self, metadata, media, lang):
        Log("TvUpdate. Lang %s" % lang)
        for season in media.seasons:
            for episode in media.seasons[season].episodes:
                for item in media.seasons[season].episodes[episode].items:
                    Log("show: %s" % media.title)
                    Log("Season: %s, Ep: %s" % (season, episode))
                    for part in item.parts:
                        Log("Release group: %s" % getReleaseGroup(part.file))
                        data = {}
                        data['sK'] = media.title
                        data['sTS'] = season
                        data['sTE'] = episode
                        data['sR'] = getReleaseGroup(part.file)
                        data['sFl'] = part.file

                        fillSeriesList()
                        #return
                        language = Prefs["langPref"]
                        Log(language)

                        subUrl = getSubUrl(data, language)
                        if not subUrl:
                            Log('Subtitle URL not found')
                            return
                        Log('Subtitle URL: '+subUrl)
                        
                        if language in part.subtitles:
                            if subUrl+'TVsubtitles.net' in part.subtitles[language]:
                                Log("Subtitle already exists")
                                return
                        Log("ready to download")
                        Log(language)
                        zipArchive = Archive.ZipFromURL(subUrl)
                        for name in zipArchive:
                            Log("Name in zip: %s" % repr(name))
                            if name[-1] == "/":
                                Log("Ignoring folder")
                                continue
                            Log(name.split(".")[-1])
                            if name.split(".")[-1] == 'srt':
                                subData = zipArchive[name]
                        #return
                        Log("Subtitle Successful download from url: "+subUrl + "  Lang: "+language)

                        part.subtitles[Locale.Language.Match(language)][subUrl+'TVsubtitles.net'] = Proxy.Media(subData, codec='srt', format='TVsubtitles.net.srt')


