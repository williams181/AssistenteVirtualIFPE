# importing the require package
import py_avataaars
from py_avataaars import PyAvataaar

# assigning various parameters to our avatar
avatar = PyAvataaar()

# Python program to create custom avatars

# importing the require package
import py_avataaars as pa

# assigning various parameters to our avatar
avatar = pa.PyAvataaar(style=pa.AvatarStyle.TRANSPARENT,
					skin_color=pa.SkinColor.LIGHT,
					hair_color=pa.HairColor.BROWN_DARK,
					facial_hair_type=pa.FacialHairType.DEFAULT,
					top_type=pa.TopType.SHORT_HAIR_DREADS_01,
					mouth_type=pa.MouthType.DEFAULT,
					eye_type=pa.EyesType.WINK_WACKY,
					eyebrow_type=pa.EyebrowType.DEFAULT_NATURAL,
					nose_type=pa.NoseType.DEFAULT,
					accessories_type=pa.AccessoriesType.DEFAULT,
					clothe_type=pa.ClotheType.BLAZER_SWEATER,
					clothe_graphic_type=pa.ClotheGraphicType.DIAMOND,)

# rendering the avatar in png format
avatar.render_png_file('data\\assistenteVirtualIFPEAvatarModelo\\avatar-IFPE-Modelo.png')
