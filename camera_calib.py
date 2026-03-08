# Import necessary libraries
import numpy as np
import cv2 as cv
import glob

class CameraCaliberation:
    def __init__(self):
        self.chessboard_size = (9, 6) # Inner corners per chessboard row and column
        self.frame_size = (1280, 720) # Size of the images used for calibration

        # Termination criteria for corner sub-pixel accuracy
        self.criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001) # Standard termination criteria from openCV

        # Prepare object points
        self.objp = np.zeros((self.chessboard_size[0]*self.chessboard_size[1], 3),np.float32)
        self.objp[:,:2] = np.mgrid[0:self.chessboard_size[0], 0:self.chessboard_size[1]].T.reshape(-1,2)

        # Arrays to store object points and image points from all the images
        self.objPoints = [] # 3d point in real world space
        self.imgPoints = [] # 2d points in image plane

    def caliberate(self, img_loc):
        # Store the list of images for calibration
        images = glob.glob(img_loc)


        for image in images:
            print(image) 
            img = cv.imread(image) # Read the image
            im_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) # Convert image to grayscale
            # cv.imshow('img', im_gray)
            # cv.waitKey(1000)
            # Finding the chessboard corners
            ret, corners = cv.findChessboardCornersSB(im_gray, self.chessboard_size, None)

            if ret == True:
                self.objPoints.append(self.objp)
                corners2 = cv.cornerSubPix(im_gray, corners, (11, 11), (-1, -1), self.criteria)
                self.imgPoints.append(corners2)

                # Draw the corners in image and display
                cv.drawChessboardCorners(img, self.chessboard_size, corners2, ret)
                cv.imshow('img', img)
                cv.waitKey(10000) # Display image for 1 second
            else:
                print("Chessboard corners not found in image: ", image)
        cv.destroyAllWindows()

        # Calibrate the camera and get the camera matrix, Distrirtion parameters, Rotation vectors, Translation vectors
        ret, cameraMatrix, distParam, rvecs, tvecs = cv.calibrateCamera(self.objPoints, self.imgPoints, self.frame_size, None, None)

        print("Camera Caliberated: ", ret)
        print("\nCamera Matrix: \n", cameraMatrix)
        print("\nDistortion Parameters: \n", distParam)
        print("\nRotation Vectors: \n", rvecs)
        print("\nTranslation Vectors: \n", tvecs)
        return cameraMatrix, distParam, rvecs, tvecs


    def undistort(self, cameraMatrix, distParam,img_dist,remap=False):
        
        # Undistort an image using the obtained caliberation parameters

        img_dist = cv.imread(img_dist)
        h, w = img_dist.shape[:2]
        newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, distParam, (w, h), 1, (w, h))
        
        if remap is False:
            # Undistort the image
            dst = cv.undistort(img_dist, cameraMatrix, distParam, None, newCameraMatrix)
            # Crop the image based on region of interest
            x, y, w, h = roi
            dst = dst[y:y+h, x:x+w]
            cv.imwrite('undistorted_image.jpg', dst)
        else:
            # Undistort with remapping
            mapx, mapy = cv.initUndistortRectifyMap(cameraMatrix, distParam, None, newCameraMatrix, (w, h), 5)
            dst_remap = cv.remap(img_dist, mapx,mapy, cv.INTER_LINEAR)

            # Crop the image based on region of interest
            x, y, w, h = roi
            dst_remap = dst_remap[y:y+h, x:x+w]
            cv.imwrite('undistorted_image_remap.jpg', dst_remap)

    def reprojection_error(self,rvecs,tvecs,cameraMatrix, distParam):
        # Reprojection Error Calculation
        mean_error = 0
        for i in range(len(self.objPoints)):
            imgPoints2, _ = cv.projectPoints(self.objPoints[i], rvecs[i], tvecs[i], cameraMatrix, distParam) 
            error = cv.norm(self.imgPoints[i], imgPoints2, cv.NORM_L2)/len(imgPoints2)
            mean_error += error
        print("\nTotal Error: {}".format(mean_error/len(self.objPoints)))
        print("\n\n\n")                


if __name__ == "__main__":
    calib = CameraCaliberation()
    cameraMatrix, distParam, rvecs, tvecs = calib.caliberate('calib_images/*.jpeg')
    calib.undistort(cameraMatrix, distParam,'calib_images/calib_image_1.jpeg',remap=True)
    calib.reprojection_error(rvecs, tvecs, cameraMatrix, distParam)