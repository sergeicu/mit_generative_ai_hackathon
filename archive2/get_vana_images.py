# query two models and get two images - cat and human 

anavitoria_rodrigueslima@fas.harvard.edu  
nemoshi@gse.harvard.edu  
vito.rodrigueslima@gmail.com

#################################
# get access code (check email)
curl -X POST https://api.vana.com/api/v0/auth/create-login \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "anavitoria_rodrigueslima@fas.harvard.edu" 
  }'
  
  
# generate a token (lasts 24 hrs apparently)  
curl -X POST https://api.vana.com/api/v0/auth/login \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "anavitoria_rodrigueslima@fas.harvard.edu",
    "code": 751910
  }'

# generate an image 
curl -X POST 'https://api.vana.com/api/v0/jobs/text-to-image' \
-H 'Authorization: Bearer eyJhbGciOiJSUzI1NiJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6InZhbmEtdXNlciIsIngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsidmFuYS11c2VyIl0sIngtaGFzdXJhLXVzZXItaWQiOiI0NDNjY2E4YS0xZWQ1LTRlYTQtOTdiYy04MjAxNTdkYTMwNmMifSwiZW1haWwiOiJhbmF2aXRvcmlhX3JvZHJpZ3Vlc2xpbWFAZmFzLmhhcnZhcmQuZWR1IiwiaWF0IjoxNjc0Nzk4NDg4LCJzdWIiOiI0NDNjY2E4YS0xZWQ1LTRlYTQtOTdiYy04MjAxNTdkYTMwNmMiLCJpc3MiOiJodHRwczovL2FwaS52YW5hLmNvbS8iLCJhdWQiOiJhcGkudmFuYS5jb20iLCJleHAiOjE2NzQ4ODQ4ODh9.CCw9yze6cemRO7hS7_kG9kFfXSUCHt-uekf2EHdRMBV__rSuugAVKNXRlKdVhKxyTxrJ2LnbNg5RUNXeYA8ZYkb4updmMvBSL5vyPZxoZHs21LDX9rHNuKjYMHE79rLaN1W1a2ThYGW_1kzg8cLP0hFieCdSBi-JQEtzLf8C7kivM1uowjpXCT-55svWPWoeKcPnTXIZL_-AxV6f5eXIujOd2CIIf7G0XryrPEO2KjJG41DWD6FY4GKmXXYSpNmB0O0woYzEDzqCXZ39PCN-R6Z0gAuclR0-6Z4TDv9JbGRLeYLd_GXe_hjVsuBqdgflNrPsrsQUSbOmfQ-Ya53nqg' \
-H 'Content-Type: application/json' \
-d '{
    "email": "anavitoria_rodrigueslima@fas.harvard.edu",
    "prompt": "{target_token} playing chess against naomi campbell closeup",
    "exhibit_name": "chess_with_naomi"
}'




# call list of exhibits 
curl https://api.vana.com/api/v0/account/exhibits \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6InZhbmEtdXNlciIsIngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsidmFuYS11c2VyIl0sIngtaGFzdXJhLXVzZXItaWQiOiI0NDNjY2E4YS0xZWQ1LTRlYTQtOTdiYy04MjAxNTdkYTMwNmMifSwiZW1haWwiOiJhbmF2aXRvcmlhX3JvZHJpZ3Vlc2xpbWFAZmFzLmhhcnZhcmQuZWR1IiwiaWF0IjoxNjc0Nzk4NDg4LCJzdWIiOiI0NDNjY2E4YS0xZWQ1LTRlYTQtOTdiYy04MjAxNTdkYTMwNmMiLCJpc3MiOiJodHRwczovL2FwaS52YW5hLmNvbS8iLCJhdWQiOiJhcGkudmFuYS5jb20iLCJleHAiOjE2NzQ4ODQ4ODh9.CCw9yze6cemRO7hS7_kG9kFfXSUCHt-uekf2EHdRMBV__rSuugAVKNXRlKdVhKxyTxrJ2LnbNg5RUNXeYA8ZYkb4updmMvBSL5vyPZxoZHs21LDX9rHNuKjYMHE79rLaN1W1a2ThYGW_1kzg8cLP0hFieCdSBi-JQEtzLf8C7kivM1uowjpXCT-55svWPWoeKcPnTXIZL_-AxV6f5eXIujOd2CIIf7G0XryrPEO2KjJG41DWD6FY4GKmXXYSpNmB0O0woYzEDzqCXZ39PCN-R6Z0gAuclR0-6Z4TDv9JbGRLeYLd_GXe_hjVsuBqdgflNrPsrsQUSbOmfQ-Ya53nqg" 
  
  
# get links to images (returns a json with many links) 
"black-and-white"  
curl https://api.vana.com/api/v0/account/exhibits/black-and-white \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6InZhbmEtdXNlciIsIngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsidmFuYS11c2VyIl0sIngtaGFzdXJhLXVzZXItaWQiOiI0NDNjY2E4YS0xZWQ1LTRlYTQtOTdiYy04MjAxNTdkYTMwNmMifSwiZW1haWwiOiJhbmF2aXRvcmlhX3JvZHJpZ3Vlc2xpbWFAZmFzLmhhcnZhcmQuZWR1IiwiaWF0IjoxNjc0Nzk4NDg4LCJzdWIiOiI0NDNjY2E4YS0xZWQ1LTRlYTQtOTdiYy04MjAxNTdkYTMwNmMiLCJpc3MiOiJodHRwczovL2FwaS52YW5hLmNvbS8iLCJhdWQiOiJhcGkudmFuYS5jb20iLCJleHAiOjE2NzQ4ODQ4ODh9.CCw9yze6cemRO7hS7_kG9kFfXSUCHt-uekf2EHdRMBV__rSuugAVKNXRlKdVhKxyTxrJ2LnbNg5RUNXeYA8ZYkb4updmMvBSL5vyPZxoZHs21LDX9rHNuKjYMHE79rLaN1W1a2ThYGW_1kzg8cLP0hFieCdSBi-JQEtzLf8C7kivM1uowjpXCT-55svWPWoeKcPnTXIZL_-AxV6f5eXIujOd2CIIf7G0XryrPEO2KjJG41DWD6FY4GKmXXYSpNmB0O0woYzEDzqCXZ39PCN-R6Z0gAuclR0-6Z4TDv9JbGRLeYLd_GXe_hjVsuBqdgflNrPsrsQUSbOmfQ-Ya53nqg" 
  
  
# download via wget / requests / 
  
  
  