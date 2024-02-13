--function Initialize()
--   print('Number of stored studies at initialization: ' .. table.getn(ParseJson(RestApiGet('/studies'))))
--end


--function Finalize()
--   print('Number of stored studies at finalization: ' .. table.getn(ParseJson(RestApiGet('/studies'))))
--end


function ReceivedInstanceFilter(dicom, origin, info)
   -- Only allow incoming MR images
   if (dicom.Modality == 'MR') then
      return true
   else
      print('Rejecting non-MR instance with modality ' .. dicom.Modality)
      return false
   end
end


function OnStoredInstance(instanceId, tags, metadata, origin)
   -- if origin['RequestOrigin'] ~= 'Lua' then
   if origin['RequestOrigin'] == 'DicomProtocol' then
      print('Instance ' .. instanceId .. ' came from ' .. origin['RemoteAet'])
      -- check if this study already has a properties file
      local study = ParseJson(RestApiGet('/instances/' .. instanceId .. '/study'))
      local allSeries = ParseJson(RestApiGet('/studies/' .. study['ID'] .. '/series'))
      local hasProperties = false
      for i, series in ipairs(allSeries) do
          local seriesDesc = series['MainDicomTags']['SeriesDescription']
          if seriesDesc == 'PROPERTIES' then
              hasProperties = true
              print('Found PROPERTIES Series: ' .. series['ID'])
          end
      end
      if not hasProperties then
          -- Create a new PROPERTIES series that holds info about the results destination
          local replace = {}
          replace['SeriesDescription'] = 'PROPERTIES'
          replace['2100-0140'] = origin['RemoteAet']  -- DestinationAE
          replace['0008,0021'] = os.date('%c')  -- SeriesDate
          replace['InstanceNumber'] = 1
          local newUID = RestApiGet('/tools/generate-uid?level=instance')
          replace['SeriesInstanceUID'] = newUID
          replace['SeriesNumber'] = 99099
          local command = {}
          command['Replace'] = replace
          command['Remove'] = {'AccessionNumber', 'ImagePositionPatient', 'ImageOrientationPatient', 'PixelData'}
          command['RemovePrivateTags'] = true
          command['Force'] = true  -- required when modifying SeriesInstanceUID
          -- Create the modified instance
          local modified = RestApiPost('/instances/' .. instanceId .. '/modify', DumpJson(command, true))
          -- Upload the modified instance to the Orthanc store
          RestApiPost('/instances/', modified)
      end
   end
end


function OnStableStudy(studyId, tags, metadata, origin)
   -- Ignore the instances that result from a modification to avoid infinite loops
   if (metadata['ModifiedFrom'] == nil and metadata['AnonymizedFrom'] == nil) then
      print('This study is now stable: ' .. studyId)

   end
end
