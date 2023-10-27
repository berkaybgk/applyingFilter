# # can read P1 and P3 files
# def read_img(f_name):
#   img = list()
#   fp = open(f_name)
#   mode=fp.readline().strip() # P3
#   fp.readline() # reads the comment
#   if mode=='P1':
#     # read black-white
#     pass
#   elif mode=='P3':
#     # read rgb file
#     r_c = fp.readline().split()
#     n_cols,n_rows = int(r_c[0]),int(r_c[1])
#     img = [[[0,0,0] for c in range(n_cols)] for r in range(n_rows)]
#     res = int(fp.readline().strip())
#     rest = fp.read()
#     rest_lst = rest.split()
#     i = 0
#     for r in range(n_rows):
#       for c in range(n_cols):
#         rgb = list()
#         for ch in range(3):
#           img[r][c][ch]=int(rest_lst[i])
#           i+=1
#   fp.close()
#   return img,res #img[r][c][p]
#
# def write_img(img,res,f_name):
#   fp = open(f_name,'w')
#   fp.write('P3\n')
#   n_rows,n_cols = len(img),len(img[0])
#   fp.write(str(n_cols)+' '+str(n_rows)+'\n')
#   fp.write(str(res)+'\n')
#   for r in range(n_rows):
#     for c in range(n_cols):
#       for ch in range(3):
#         fp.write(str(img[r][c][ch])+' ')
#       fp.write('\t')
#     fp.write('\n')
#   fp.close()
#
# def rec_color(img,r,c,res,col):
#   n_rows,n_cols=len(img),len(img[0])
#   if r<0 or c <0 or r>=n_rows or c>=n_cols: # check out actual borders
#     return
#   if not img[r][c] == [res,res,res]:
#     return
#   img[r][c] = col
#   neigh_list=[[-1,0],[+1,0],[0,-1],[0,+1]]
#   for neigh in neigh_list:
#     rec_color(img,r+neigh[0],c+neigh[1],res,col)
#
#
# def apply_coloring(img,res):
#   colors=[[res,0,0],[0,res,0],[0,0,res],[res,res,0],[res,0,res],[res//2,res//2,0]]
#   next_color=0
#   n_rows,n_cols=len(img),len(img[0])
#   for r in range(n_rows):
#     for c in range(n_cols):
#       if img[r][c] == [res,res,res]: # is white (not colored before, not wall)
#         rec_color(img,r,c,res,colors[next_color])
#         next_color = (next_color+1)%len(colors)
#   return img
#
# f_name='walls.ppm'
# img,res = read_img(f_name)
# img = apply_coloring(img,res)
# write_img(img,res,f_name[:-4]+'_colored.ppm')
#

# print(int(17.311//1))



# On PPM and PGM formats see http://paulbourke.net/dataformats/ppm/
# On convolution operation see https://youtu.be/KiftWz544_8
# To view .pgm and .ppm files, you can use IrfanView, see https://www.irfanview.com/
# To check whether your outputs are the same as ours, you can use the same techniques as in Homework 2, or you can write your own code.

filename = input()
operation = int(input())


def img_printer(img):
    row = len(img)
    col = len(img[0])
    cha = len(img[0][0])
    for i in range(row):
        for j in range(col):
            for k in range(cha):
                print(img[i][j][k], end=" ")
            print("\t|", end=" ")
        print()


# DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE

file_handle = open(filename)
image_format = file_handle.readline().strip()
row_count, col_count = file_handle.readline().strip().split()
row_count = int(row_count)
col_count = int(col_count)
max_color_value = file_handle.readline().strip()
rest_list = file_handle.readlines()


if operation == 1:

    if len(rest_list) >= row_count+10:
        for element_index in range(len(rest_list)):
            rest_list[element_index] = rest_list[element_index].strip()

        temp_list = []
        for row_c in range(row_count):
            temp_row_list = []
            for col_c in range(col_count):
                temp_row_list.append([rest_list[(row_c*row_count)+col_c]])
            temp_list.append(temp_row_list)

        rest_list = temp_list.copy()

    else:
        for row_str in range(len(rest_list)):
            rest_list[row_str] = rest_list[row_str].replace("\t", " ").strip().split()
            for element_index in range(int(col_count)):
                rest_list[row_str][element_index] = [rest_list[row_str][element_index]]

    is_added_list = [["F" for i in range(col_count)] for j in range(col_count)]
    for r in range(row_count):
        for c in range(col_count):
            if rest_list[r][c][0] == "0":
                is_added_list[r][c] = "T"

    is_painted_list = [["F" for i in range(col_count)] for j in range(col_count)]
    for r in range(row_count):
        for c in range(col_count):
            if rest_list[r][c][0] == "0":
                is_painted_list[r][c] = "T"

    current_sum = 0
    num_pixels = 0
    new_list = rest_list.copy()


    def average_finder(three_d_img, r, c):
        global is_added_list
        global current_sum
        global num_pixels
        n_row = len(three_d_img)
        n_col = len(three_d_img[0])

        if not ((r < n_row) and (c < n_col) and (r >= 0) and (c >= 0)):
            return
        if is_added_list[r][c] == "T":
            return

        neigh_list = [[-1, 0], [+1, 0], [0, -1], [0, +1]]
        if (r < n_row) and (c < n_col) and (r >= 0) and (c >= 0):
            if not is_added_list[r][c] == "T":
                current_sum += int(three_d_img[r][c][0])
                num_pixels += 1
                is_added_list[r][c] = "T"
                for neigh in neigh_list:
                    average_finder(three_d_img, r + neigh[0], c + neigh[1])
        return current_sum // num_pixels


    def rec_color(list_wbcolored, r, c, col_code):
        global is_painted_list

        n_row = len(list_wbcolored)
        n_col = len(list_wbcolored[0])

        if not ((r < n_row) and (c < n_col) and (r >= 0) and (c >= 0)):
            return
        if is_painted_list[r][c] == "T":
            return

        neigh_list = [[-1, 0], [+1, 0], [0, -1], [0, +1]]
        if (r < n_row) and (c < n_col) and (r >= 0) and (c >= 0):
            if not is_painted_list[r][c] == "T":
                list_wbcolored[r][c] = [f"{col_code}"]
                is_painted_list[r][c] = "T"
                for neigh in neigh_list:
                    rec_color(list_wbcolored, r + neigh[0], c + neigh[1], col_code)
        return list_wbcolored


    for r in range(row_count):
        for c in range(col_count):
            if is_painted_list[r][c] == "F":
                col_value = average_finder(rest_list, r, c)
                rec_color(new_list, r, c, col_value)
                current_sum = 0
                num_pixels = 0

    img_printer(new_list)

if operation == 2:

    filename_filter = input()
    stride_parameter = int(input())

    filter_handle = open(filename_filter)
    filter_list = filter_handle.readlines()

    for ind in range(len(filter_list)):
        filter_list[ind] = filter_list[ind].strip().split()

    for row_str in range(len(rest_list)):
        rest_list[row_str] = rest_list[row_str].replace("\t", " ").strip().split("  ")
        for element_index in range(int(col_count)):
            rest_list[row_str][element_index] = rest_list[row_str][element_index].strip().split()


    new_list3 = [[["" for i in range(3)] for j in range(col_count)] for k in range(row_count)]
    n_row = len(rest_list)
    n_col = len(rest_list[0])


    def recursive_filter(threed_img, r, c, filter_list2d, direction = "r"):
        global n_row
        global n_col
        global new_list3
        global stride_parameter

        width = int(len(filter_list2d)//2)

        if r >= n_row - width: # base condition, if rows has ended end columns are finished

            if direction == "r" and c >= n_col - width:
                return
            elif direction == "l" and c < width:
                return


        else: # if convolution is not to end, keep going

            if direction == "r" and c == n_col - width: # end of the columns,going right
                recursive_filter(threed_img, r+1, c-stride_parameter,filter_list2d,"l")

            elif direction == "l" and c < width: # at the start of the row while coming to the right
                recursive_filter(threed_img, r+1, c+stride_parameter,filter_list2d,"r")

            else:

                # weighted sum operation
                neighbours = []
                for i in range(-1 * width, width + 1):
                    for j in range(-1 * width, width + 1):
                        neighbours.append([r + i, c + j])

                total_temp_red = 0
                total_temp_green = 0
                total_temp_blue = 0

                for filter_row in range(len(filter_list2d)):
                    for filter_col in range(len(filter_list2d[0])):
                        temp_row = neighbours[(filter_row * len(filter_list2d) + filter_col)][0]
                        temp_col = neighbours[(filter_row * len(filter_list2d) + filter_col)][1]

                        total_temp_red += int(threed_img[temp_row][temp_col][0]) * float(filter_list2d[filter_row][filter_col])
                        total_temp_green += int(threed_img[temp_row][temp_col][1]) * float(filter_list2d[filter_row][filter_col])
                        total_temp_blue += int(threed_img[temp_row][temp_col][2]) * float(filter_list2d[filter_row][filter_col])

                red_wbp = int(total_temp_red // 1)
                green_wbp = int(total_temp_green // 1)
                blue_wbp = int(total_temp_blue // 1)

                new_list3[r][c][0] = str(red_wbp) if (red_wbp >= 0 and red_wbp <= 255) else ("0" if red_wbp < 0 else "255")
                new_list3[r][c][1] = str(green_wbp) if (green_wbp >= 0 and green_wbp <= 255) else ("0" if green_wbp < 0 else "255")
                new_list3[r][c][2] = str(blue_wbp) if (blue_wbp >= 0 and blue_wbp <= 255) else ("0" if blue_wbp < 0 else "255")

                if r < width: # if rows are not enough to apply filter
                    recursive_filter(threed_img, r+1, c, filter_list2d, direction)

                elif c < width: # if columns are not enough to apply filter
                    recursive_filter(threed_img, r, c+1, filter_list2d, direction)

                elif (r >= width) and (r < (n_row - width)) and (c >= width) and (c < (n_col - width)) and direction == "r":
                    recursive_filter(threed_img, r, c + stride_parameter, filter_list2d, direction)

                elif (r >= width) and (r < (n_row - width)) and (c >= width) and (c < (n_col - width)) and direction == "l":
                    recursive_filter(threed_img, r, c - stride_parameter, filter_list2d, direction)


    recursive_filter(rest_list, 0, 0, filter_list)

    if new_list3[0][0] == ["0","0","0"]:
        new_list3[0][0] = ["", "", ""]

    list_wbp = []
    row_ind = 0
    col_ind = 0

    for last_row in range(len(new_list3)):
        row_lst_temp = []
        for last_col in range(len(new_list3[last_row])):
            if not new_list3[last_row][last_col] == ['', '', '']:
                row_lst_temp.append(new_list3[last_row][last_col])
        list_wbp.append(row_lst_temp)

    for i in range(int(len(filter_list)//2)):
        list_wbp.pop(0)
        list_wbp.pop()
    for k in range(int(len(filter_list) // 2)):
        list_wbp[0].pop(0)

    img_printer(list_wbp)
    filter_handle.close()

file_handle.close()


# DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE

