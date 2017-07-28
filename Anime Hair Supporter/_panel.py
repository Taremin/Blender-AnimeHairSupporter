import bpy

class VIEW3D_PT_tools_anime_hair_supporter(bpy.types.Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = 'Tools'
	bl_context = 'objectmode'
	bl_label = "アニメ髪支援"
	bl_options = {'DEFAULT_CLOSED'}
	
	def draw(self, context):
		row = self.layout.row(align=True)
		row.operator('object.ahs_meshedge_to_curve', icon='CURVE_NCURVE')
		row.enabled = len([o for o in context.selected_objects if o.type == 'MESH'])
		
		
		# メインカーブ
		box = self.layout.box()
		box.label("メインカーブ", icon='MAN_ROT')
		
		# 肉付け関係
		row = box.row(align=True)
		row.operator('object.ahs_maincurve_fleshout', icon='MESH_CAPSULE')
		row.operator('object.ahs_maincurve_fleshlose', text="", icon='X')
		
		# 余剰変形
		box.operator('object.ahs_maincurve_surplus_transform', icon='CURVE_NCURVE')
		
		# サブツール
		column = box.column(align=True)
		row = column.row(align=True)
		row.operator('object.ahs_maincurve_select', icon='RESTRICT_SELECT_OFF')
		row.operator('object.ahs_maincurve_hide', text="表示", icon='VISIBLE_IPO_ON').is_hide = False
		row.operator('object.ahs_maincurve_hide', text="隠す", icon='VISIBLE_IPO_OFF').is_hide = True
		
		# 解像度
		row = column.row(align=True)
		try: is_successed = context.active_object.data.taper_object and context.active_object.data.bevel_object and context.active_object.data.splines.active
		except: is_successed = False
		if is_successed: row.prop(context.active_object.data.splines.active, 'resolution_u', text="解像度")
		else: row.label(text="解像度:")
		# 次数
		try: is_successed = context.active_object.data.taper_object and context.active_object.data.bevel_object and context.active_object.data.splines.active
		except: is_successed = False
		if is_successed: row.prop(context.active_object.data.splines.active, 'order_u', text="次数")
		else: row.label(text="次数:")
		
		
		# テーパーカーブ
		box = self.layout.box()
		box.label("テーパーカーブ", icon='CURVE_NCURVE')
		
		# 位置を再設定
		row = box.row(align=True)
		row.operator('object.ahs_tapercurve_move', icon='PARTICLE_TIP').mode = 'TAPER'
		row.operator('object.ahs_tapercurve_move', text="", icon='OUTLINER_DATA_ARMATURE').mode = 'BOTH'
		
		# サブツール
		column = box.column(align=True)
		row = column.row(align=True)
		row.operator('object.ahs_tapercurve_select', icon='RESTRICT_SELECT_OFF').is_bevel = False
		op = row.operator('object.ahs_tapercurve_hide', text="表示", icon='VISIBLE_IPO_ON')
		op.is_bevel, op.is_hide = False, False
		op = row.operator('object.ahs_tapercurve_hide', text="隠す", icon='VISIBLE_IPO_OFF')
		op.is_bevel, op.is_hide = False, True
		
		# 解像度
		try:
			column.prop(context.active_object.data.taper_object.data.splines.active, 'resolution_u', text="解像度")
			is_successed = True
		except: is_successed = False
		if not is_successed:
			taper_objects = [c.taper_object for c in context.blend_data.curves if c.taper_object]
			try:
				if context.active_object in taper_objects:
					column.prop(context.active_object.data.splines.active, 'resolution_u', text="解像度")
					is_successed = True
			except: is_successed = False
		if not is_successed: column.label(text="解像度:")
		
		
		# ベベルカーブ
		box = self.layout.box()
		box.label("ベベルカーブ", icon='SURFACE_NCIRCLE')
		
		# 位置を再設定
		row = box.row(align=True)
		row.operator('object.ahs_tapercurve_move', icon='PARTICLE_TIP').mode = 'BEVEL'
		row.operator('object.ahs_tapercurve_move', text="", icon='OUTLINER_DATA_ARMATURE').mode = 'BOTH'
		
		# サブツール
		column = box.column(align=True)
		row = column.row(align=True)
		row.operator('object.ahs_tapercurve_select', icon='RESTRICT_SELECT_OFF').is_bevel = True
		op = row.operator('object.ahs_tapercurve_hide', text="表示", icon='VISIBLE_IPO_ON')
		op.is_bevel, op.is_hide = True, False
		op = row.operator('object.ahs_tapercurve_hide', text="隠す", icon='VISIBLE_IPO_OFF')
		op.is_bevel, op.is_hide = True, True
		
		# 解像度
		try:
			column.prop(context.active_object.data.bevel_object.data.splines.active, 'resolution_u', text="解像度")
			is_successed = True
		except: is_successed = False
		if not is_successed:
			bevel_objects = [c.bevel_object for c in context.blend_data.curves if c.bevel_object]
			try:
				if context.active_object in bevel_objects:
					column.prop(context.active_object.data.splines.active, 'resolution_u', text="解像度")
					is_successed = True
			except: is_successed = False
		if not is_successed: column.label(text="解像度:")
		
		
		row = self.layout.row(align=True)
		row.operator('object.convert', text="メッシュ化", icon='MESH_ICOSPHERE').target = 'MESH'
		for ob in context.selected_objects:
			if ob.type != 'CURVE': continue
			if ob.data.taper_object and ob.data.bevel_object:
				row.enabled = True
				break
		else: row.enabled = False