import create_verbs as crv

verbs = {}

verb = "walking"
fn_video_mov = f"./IMG_2455.MOV"
root_save_A = "./imgs2_in/"
flag_create_frames = False
if flag_create_frames:
    n_images = crv.video_to_frames(\
        fn_video_mov,root_save_A)
fn_save_verb_txt = f"./JGE-{verb}-motion.txt"
root_save_B = "./imgs2_out/"
flag_create_motion = True
if flag_create_motion:
    n_images=crv.frames_to_motion(root_save_B,
                fn_save_verb_txt)
scale = .5
w = int(1080*scale)
h = int(1920*scale)
c = 3
verbs,n_images = crv.add_motion_to_verbs(\
    verbs, fn_save_verb_txt,verb, w,h)
fn_video = f'./verb-{verb}-001.avi'
crv.verb_to_video(verbs,verb,fn_video,w,h,c,
              n_images)

