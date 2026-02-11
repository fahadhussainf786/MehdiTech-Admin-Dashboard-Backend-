# import asyncio
# from datetime import datetime
# from supabase import create_client
# import os

# supabase = create_client(
#     os.getenv("SUPABASE_URL"),
#     os.getenv("SUPABASE_SERVICE_ROLE_KEY")
# )

# # background loop
# async def auto_publish_blogs():
#     while True:
#         now = datetime.utcnow()   # current UTC time

#         # get scheduled blogs whose time passed
#         blogs = supabase.table("blogs") \
#             .select("id") \
#             .eq("status", "scheduled") \
#             .lte("publish_at", now) \
#             .execute()

#         # update them to live
#         for blog in blogs.data:
#             supabase.table("blogs").update({
#                 "status": "live"
#             }).eq("id", blog["id"]).execute()

#         await asyncio.sleep(3)  # check every 1 minute
