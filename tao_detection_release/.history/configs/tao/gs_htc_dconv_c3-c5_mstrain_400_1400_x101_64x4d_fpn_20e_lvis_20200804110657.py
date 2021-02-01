# model settings
model = dict(
    type='HybridTaskCascade',
    num_stages=3,
    pretrained='open-mmlab://resnext101_64x4d',
    interleaved=True,
    mask_info_flow=True,
    backbone=dict(
        type='ResNeXt',
        depth=101,
        groups=64,
        base_width=4,
        num_stages=4,
        out_indices=(0, 1, 2, 3),
        frozen_stages=1,
        style='pytorch',
        dcn=dict(
            modulated=False,
            groups=64,
            deformable_groups=1,
            fallback_on_stride=False),
        stage_with_dcn=(False, True, True, True)),
    neck=dict(
        type='FPN',
        in_channels=[256, 512, 1024, 2048],
        out_channels=256,
        num_outs=5),
    rpn_head=dict(
        type='RPNHead',
        in_channels=256,
        feat_channels=256,
        anchor_scales=[8],
        anchor_ratios=[0.5, 1.0, 2.0],
        anchor_strides=[4, 8, 16, 32, 64],
        target_means=[.0, .0, .0, .0],
        target_stds=[1.0, 1.0, 1.0, 1.0],
        loss_cls=dict(
            type='CrossEntropyLoss', use_sigmoid=True, loss_weight=1.0),
        loss_bbox=dict(type='SmoothL1Loss', beta=1.0 / 9.0, loss_weight=1.0)),
    bbox_roi_extractor=dict(
        type='SingleRoIExtractor',
        roi_layer=dict(type='RoIAlign', out_size=7, sample_num=2),
        out_channels=256,
        featmap_strides=[4, 8, 16, 32]),
    bbox_head=[
        dict(
            type='GSBBoxHeadWith0',
            num_fcs=2,
            in_channels=256,
            fc_out_channels=1024,
            gs_config=dict(
                label2binlabel='./data/lvis/label2binlabel.pt',
                pred_slice='./data/lvis/pred_slice_with0.pt',
                fg_split='./data/lvis/valsplit.pkl',
                others_sample_ratio=8.0,
                loss_bg=dict(
                    type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0
                ),
                num_bins=5,
                loss_bin=dict(
                    type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0
                ),
            ),
            roi_feat_size=7,
            num_classes=1231,
            target_means=[0., 0., 0., 0.],
            target_stds=[0.1, 0.1, 0.2, 0.2],
            reg_class_agnostic=True,
            loss_cls=dict(
                type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0),
            loss_bbox=dict(type='SmoothL1Loss', beta=1.0, loss_weight=1.0)),
        dict(
            type='GSBBoxHeadWith0',
            num_fcs=2,
            in_channels=256,
            fc_out_channels=1024,
            gs_config=dict(
                label2binlabel='./data/lvis/label2binlabel.pt',
                pred_slice='./data/lvis/pred_slice_with0.pt',
                fg_split='./data/lvis/valsplit.pkl',
                others_sample_ratio=8.0,
                loss_bg=dict(
                    type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0
                ),
                num_bins=5,
                loss_bin=dict(
                    type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0
                ),
            ),
            roi_feat_size=7,
            num_classes=1231,
            target_means=[0., 0., 0., 0.],
            target_stds=[0.05, 0.05, 0.1, 0.1],
            reg_class_agnostic=True,
            loss_cls=dict(
                type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0),
            loss_bbox=dict(type='SmoothL1Loss', beta=1.0, loss_weight=1.0)),
        dict(
            type='GSBBoxHeadWith0',
            num_fcs=2,
            in_channels=256,
            fc_out_channels=1024,
            gs_config=dict(
                label2binlabel='./data/lvis/label2binlabel.pt',
                pred_slice='./data/lvis/pred_slice_with0.pt',
                fg_split='./data/lvis/valsplit.pkl',
                others_sample_ratio=8.0,
                loss_bg=dict(
                    type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0
                ),
                num_bins=5,
                loss_bin=dict(
                    type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0
                ),
            ),
            roi_feat_size=7,
            num_classes=1231,
            target_means=[0., 0., 0., 0.],
            target_stds=[0.033, 0.033, 0.067, 0.067],
            reg_class_agnostic=True,
            loss_cls=dict(
                type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0),
            loss_bbox=dict(type='SmoothL1Loss', beta=1.0, loss_weight=1.0))
    ],
    mask_roi_extractor=dict(
        type='SingleRoIExtractor',
        roi_layer=dict(type='RoIAlign', out_size=14, sample_num=2),
        out_channels=256,
        featmap_strides=[4, 8, 16, 32]),
    mask_head=dict(
        type='HTCMaskHead',
        num_convs=4,
        in_channels=256,
        conv_out_channels=256,
        num_classes=1231,
        loss_mask=dict(
            type='CrossEntropyLoss', use_mask=True, loss_weight=1.0)),
    semantic_roi_extractor=dict(
        type='SingleRoIExtractor',
        roi_layer=dict(type='RoIAlign', out_size=14, sample_num=2),
        out_channels=256,
        featmap_strides=[8]),
    semantic_head=dict(
        type='FusedSemanticHead',
        num_ins=5,
        fusion_level=1,
        num_convs=4,
        in_channels=256,
        conv_out_channels=256,
        num_classes=183,
        ignore_label=255,
        loss_weight=0.2))
# model training and testing settings
train_cfg = dict(
    rpn=dict(
        assigner=dict(
            type='MaxIoUAssigner',
            pos_iou_thr=0.7,
            neg_iou_thr=0.3,
            min_pos_iou=0.3,
            ignore_iof_thr=-1),
        sampler=dict(
            type='RandomSampler',
            num=256,
            pos_fraction=0.5,
            neg_pos_ub=-1,
            add_gt_as_proposals=False),
        allowed_border=0,
        pos_weight=-1,
        debug=False),
    rpn_proposal=dict(
        nms_across_levels=False,
        nms_pre=2000,
        nms_post=2000,
        max_num=2000,
        nms_thr=0.7,
        min_bbox_size=0),
    rcnn=[
        dict(
            assigner=dict(
                type='MaxIoUAssigner',
                pos_iou_thr=0.5,
                neg_iou_thr=0.5,
                min_pos_iou=0.5,
                ignore_iof_thr=-1),
            sampler=dict(
                type='RandomSampler',
                num=512,
                pos_fraction=0.25,
                neg_pos_ub=-1,
                add_gt_as_proposals=True),
            mask_size=28,
            pos_weight=-1,
            debug=False),
        dict(
            assigner=dict(
                type='MaxIoUAssigner',
                pos_iou_thr=0.6,
                neg_iou_thr=0.6,
                min_pos_iou=0.6,
                ignore_iof_thr=-1),
            sampler=dict(
                type='RandomSampler',
                num=512,
                pos_fraction=0.25,
                neg_pos_ub=-1,
                add_gt_as_proposals=True),
            mask_size=28,
            pos_weight=-1,
            debug=False),
        dict(
            assigner=dict(
                type='MaxIoUAssigner',
                pos_iou_thr=0.7,
                neg_iou_thr=0.7,
                min_pos_iou=0.7,
                ignore_iof_thr=-1),
            sampler=dict(
                type='RandomSampler',
                num=512,
                pos_fraction=0.25,
                neg_pos_ub=-1,
                add_gt_as_proposals=True),
            mask_size=28,
            pos_weight=-1,
            debug=False)
    ],
    stage_loss_weights=[1, 0.5, 0.25])
test_cfg = dict(
    rpn=dict(
        nms_across_levels=False,
        nms_pre=1000,
        nms_post=1000,
        max_num=1000,
        nms_thr=0.7,
        min_bbox_size=0),
    rcnn=dict(
        score_thr=0.00001,
        nms=dict(type='nms', iou_thr=0.95),
        max_per_img=500, # 100, 300
        mask_thr_binary=0.5),
    keep_all_stages=False)
# dataset settings
dataset_type = 'TaoDataset'
data_root = '/home/songbai.xb/workspace/projects/TAO/data/TAO/'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='LoadAnnotations', with_bbox=True, with_mask=True, with_seg=True, poly2mask=False),
    dict(
        type='Resize',
        img_scale=[(1600, 400), (1600, 1400)],
        multiscale_mode='range',
        keep_ratio=True),
    dict(type='RandomFlip', flip_ratio=0.5),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='Pad', size_divisor=32),
    dict(type='SegResizeFlipPadRescale', scale_factor=1 / 8),
    dict(type='DefaultFormatBundle'),
    dict(
        type='Collect',
        keys=['img', 'gt_bboxes', 'gt_labels', 'gt_masks', 'gt_semantic_seg']),
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(1333, 800),
        img_scale=[(1333, 800), (1600,960)],
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip', flip_ratio=0.5),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='Pad', size_divisor=32),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img']),
        ])
]
data = dict(
    imgs_per_gpu=1,
    workers_per_gpu=1,
    train=dict(
        type=dataset_type,
        ann_file=data_root + 'lvis_v0.5_train.json',
        img_prefix=data_root + 'train2017/',
        seg_prefix=data_root + 'stuffthingmaps/train2017/',
        pipeline=train_pipeline),
    val=dict(
        type=dataset_type,
        ann_file=data_root + 'annotations/validation_amend.json',
        img_prefix=data_root + 'frames/',
        pipeline=test_pipeline),
    test=dict(
        type=dataset_type,
        ann_file=data_root + 'annotations/validation_amend.json',
        img_prefix=data_root + 'frames/',
        pipeline=test_pipeline))
# optimizer
optimizer = dict(type='SGD', lr=0.005, momentum=0.9, weight_decay=0.0001)
optimizer_config = dict(grad_clip=dict(max_norm=35, norm_type=2))
# learning policy
lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=500,
    warmup_ratio=1.0 / 3,
    step=[8, 11])
checkpoint_config = dict(interval=1)
# yapf:disable
log_config = dict(
    interval=50,
    hooks=[
        dict(type='TextLoggerHook'),
        # dict(type='TensorboardLoggerHook')
    ])
# yapf:enable
# runtime settings
total_epochs = 12
dist_params = dict(backend='nccl')
log_level = 'INFO'
work_dir = './work_dirs/gs_htc_dconv_c3-c5_mstrain_400_1400_x101_64x4d_fpn_20e_lvis_lrdown'
load_from = './data/weneed/htc_x101_msdcn/epoch_20.pth'
resume_from = None
workflow = [('train', 1)]

# Train which part, 0 for all, 1 for cls, 2 for bbox_head, 3 for cascade cls
selectp = 3
